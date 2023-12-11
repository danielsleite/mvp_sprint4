from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Paciente, Model
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
paciente_tag = Tag(
    name="Paciente",
    description="Adição, visualização, remoção e predição de pacientes com Diabetes",
)


# Rota home
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


# Rota de listagem de pacientes
@app.get(
    "/pacientes",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "404": ErrorSchema},
)
def get_pacientes():
    """Lista todos os pacientes cadastrados na base
    Retorna uma lista de pacientes cadastrados na base.

    Args:
        Id (int): id do paciente

    Returns:
        list: lista de pacientes cadastrados na base
    """
    session = Session()

    # Buscando todos os pacientes
    pacientes = session.query(Paciente).all()

    if not pacientes:
        logger.warning("Não há pacientes cadastrados na base :/")
        return {"message": "Não há pacientes cadastrados na base :/"}, 404
    else:
        logger.debug(f"%d pacientes econtrados" % len(pacientes))
        return apresenta_pacientes(pacientes), 200


# Rota de adição de paciente
@app.post(
    "/paciente",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "400": ErrorSchema, "409": ErrorSchema},
)
def predict(form: PacienteSchema):
    """Adiciona um novo paciente à base de dados
    Retorna uma representação dos pacientes e diagnósticos associados.

    Args:


        age (int): idade do paciente [anos]
        sex (String): sexo do paciente [M: masculino ou F: feminino]
        shestpaintype (String): tipo de dor torácica [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic]
        restingbp (int): pressão arterial em repouso [mm Hg]
        cholesterol (int): Colesterol Sérico [mm/dl]
        fastingbs (int): Glicemia em Jejum [1: if FastingBS > 120 mg/dl, 0: otherwise]
        restingecg (string): Resultados do Eletrocardiograma em Repouso [Normal: Normal, ST: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV), LVH: showing probable or definite left ventricular hypertrophy by Estes' criteria]
        maxhr (float): Frequência Cardíaca Máxima Alcançada [valor numérico entre 60 e 202]
        exerciseangina (string): Angina Induzida por Exercício [Y: Yes, N: No]
        oldpeak (float): Oldpeak ST ST [Valor numérico medido na depressão]
        st_slope (string): Inclinação do Segmento ST do Pico do Exercício [Up: upsloping, Flat: flat, Down: downsloping]

    Returns:
        dict: representação do paciente e diagnóstico associado
    """

    # Carregando modelo
    ml_path = "ml_model/classificador.pkl"
    scaler_path = "ml_model/scaler.pkl"
    dict_path = "ml_model/dicionario.pkl"
    model = Model(ml_path, scaler_path, dict_path)

    paciente = Paciente(
        age=form.age,
        sex=form.sex,
        shestpaintype=form.shestpaintype,
        restingbp=form.restingbp,
        cholesterol=form.cholesterol,
        fastingbs=form.fastingbs,
        restingecg=form.restingecg,
        maxhr=form.maxhr,
        exerciseangina=form.exerciseangina,
        oldpeak=form.oldpeak,
        st_slope=form.st_slope,
        diagnostico=model.preditor(form),
    )
    logger.debug(f"Adicionando produto de nome: '{paciente.id}'")

    try:
        # Criando conexão com a base
        session = Session()

        # # Checando se paciente já existe na base
        # if session.query(Paciente).filter(Paciente.id == form.id).first():
        #     error_msg = "Paciente já existente na base :/"
        #     logger.warning(f"Erro ao adicionar paciente '{paciente.id}', {error_msg}")
        #     return {"message": error_msg}, 409

        # Adicionando paciente
        session.add(paciente)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado paciente de ID: '{paciente.id}'")
        return apresenta_paciente(paciente), 200

    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar paciente id: '{paciente.id}', {error_msg}")
        return {"message": error_msg}, 400


# Rota de adição diagnóstico
@app.post(
    "/diagnostico",
    tags=[paciente_tag],
    responses={
        "200": PacienteDiagnosticoSchema,
        "400": ErrorSchema,
        "409": ErrorSchema,
    },
)
def diag(form: PacienteSchema):
    """Realiza o diagnóstico do paciente, sem salvar na base de dados
    Retorna o diagnóstico 0 - em doença, 1 - com doença.

    Args:


        age (int): idade do paciente [anos]
        sex (String): sexo do paciente [M: masculino ou F: feminino]
        shestpaintype (String): tipo de dor torácica [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic]
        restingbp (int): pressão arterial em repouso [mm Hg]
        cholesterol (int): Colesterol Sérico [mm/dl]
        fastingbs (int): Glicemia em Jejum [1: if FastingBS > 120 mg/dl, 0: otherwise]
        restingecg (string): Resultados do Eletrocardiograma em Repouso [Normal: Normal, ST: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV), LVH: showing probable or definite left ventricular hypertrophy by Estes' criteria]
        maxhr (float): Frequência Cardíaca Máxima Alcançada [valor numérico entre 60 e 202]
        exerciseangina (string): Angina Induzida por Exercício [Y: Yes, N: No]
        oldpeak (float): Oldpeak ST ST [Valor numérico medido na depressão]
        st_slope (string): Inclinação do Segmento ST do Pico do Exercício [Up: upsloping, Flat: flat, Down: downsloping]

    Returns:
        int: representação do paciente e diagnóstico associado
    """

    # Carregando modelo
    ml_path = "ml_model/classificador.pkl"
    scaler_path = "ml_model/scaler.pkl"
    dict_path = "ml_model/dicionario.pkl"
    model = Model(ml_path, scaler_path, dict_path)

    paciente = Paciente(
        age=form.age,
        sex=form.sex,
        shestpaintype=form.shestpaintype,
        restingbp=form.restingbp,
        cholesterol=form.cholesterol,
        fastingbs=form.fastingbs,
        restingecg=form.restingecg,
        maxhr=form.maxhr,
        exerciseangina=form.exerciseangina,
        oldpeak=form.oldpeak,
        st_slope=form.st_slope,
        diagnostico=model.preditor(form),
    )
    logger.debug(f"Adicionando produto de nome: '{paciente.id}'")

    try:
        logger.debug(f"Adicionado paciente de ID: '{paciente.id}'")
        return {"diagnostico": paciente.diagnostico}, 200

    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar paciente id: '{paciente.id}', {error_msg}")
        return {"message": error_msg}, 400


# Métodos baseados em id
# Rota de busca de paciente por id
@app.get(
    "/paciente",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "404": ErrorSchema},
)
def get_paciente(query: PacienteBuscaSchema):
    """Faz a busca por um paciente cadastrado na base a partir do nome

    Args:
        id (int): id do paciente

    Returns:
        dict: representação do paciente e diagnóstico associado
    """

    paciente_id = query.id
    logger.debug(f"Coletando dados sobre produto #{paciente_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    paciente = session.query(Paciente).filter(Paciente.id == paciente_id).first()

    if not paciente:
        # se o paciente não foi encontrado
        error_msg = f"Paciente {paciente_id} não encontrado na base :/"
        logger.warning(f"Erro ao buscar paciente com id:  '{paciente_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Paciente econtrado, id: '{paciente.id}'")
        # retorna a representação do paciente
        return apresenta_paciente(paciente), 200


# Rota de remoção de paciente por id
@app.delete(
    "/paciente",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "404": ErrorSchema},
)
def delete_paciente(query: PacienteBuscaSchema):
    """Remove um paciente cadastrado na base a partir do nome

    Args:
        id (int): id do paciente

    Returns:
        msg: Mensagem de sucesso ou erro
    """

    paciente_id = query.id
    logger.debug(f"Deletando dados sobre paciente de id: #{paciente_id}")

    # Criando conexão com a base
    session = Session()

    # Buscando paciente
    paciente = session.query(Paciente).filter(Paciente.id == paciente_id).first()

    if not paciente:
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao deletar paciente id: '{paciente_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(paciente)
        session.commit()
        logger.debug(f"Deletado paciente #{paciente_id}")
        return {"message": f"Paciente {paciente_id} removido com sucesso!"}, 200
