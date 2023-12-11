# API para predição de problemas de coração

Esse projeto apresenta o MVP de requisido para conclusão da sprint 4 da curso de  **Engenharia de Softaware**  oferecido pela **PUC-Rio**

Para tal, foi criado uma API em python, utilizando como base as bibliotecas flask e sqlalchemy. 

Essa API tem como objetivo demosntrar o uso de ferramentas de aprendizado de máquina para realizar classificação de dados.

A base de dados utilizada para predição é uma base pública com dados anonimizados e pode ser obtida pelo [link](https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction/data)

Para a classficação de pacientes com ou sem doença cardíaca, o modelo faz uso dos seguintes argumentos:

>**age (int):** idade do paciente [anos]

>**sex (String):** sexo do paciente [M: masculino ou F: feminino]

>**shestpaintype (String):** tipo de dor torácica [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic]

>**restingbp (int):** pressão arterial em repouso [mm Hg]

>**cholesterol (int):** Colesterol Sérico [mm/dl]

>**fastingbs (int):** Glicemia em Jejum [1: if FastingBS > 120 mg/dl, 0: otherwise]

>**restingecg (string):** Resultados do Eletrocardiograma em Repouso [Normal: Normal, ST: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV), LVH: showing probable or definite left ventricular hypertrophy by Estes' criteria] 

>**maxhr (float):** Frequência Cardíaca Máxima Alcançada [valor numérico entre 60 e 202]

>**exerciseangina (string):** Angina Induzida por Exercício [Y: Yes, N: No]

>**oldpeak (float):** Oldpeak ST ST [Valor numérico medido na depressão]

>**st_slope (string):**  Inclinação do Segmento ST do Pico do Exercício [Up: upsloping, Flat: flat, Down: downsloping]

---
## Saída

O resultado da classificação será um valor inteiro, pode pode assuimr dois valores:

* 0 - Classificado sem problema cardíado 
* 1 - Classificado com problema cardíaco.

---

## Banco

Para realizar a rentenção dos dados, a API cria um banco .sqlite3, caso o mesmo não exista.

O Banco, possuio a tabela `paciente`, que armazena os campos os dados de entrada do classificador e a saída predita.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements_api.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).



```
(env)$ pip install -r requirements_api.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements_api.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução nas três vesões disponíveis (Sswagger, ReDoc, RapiDoc).

Para versão `Swagger` abra o link [http://localhost:5000/openapi/swagger#/](http://localhost:5000/openapi/swagger#/) no navegador



Uma vez executando, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador.


---
## Notebook

Na posta notebook desse repositório, se encontra o notebook utlizado para desenvolvimento do modelo de classficação, bem como a exporatção dos dados desse modelo para o uso nessa aplciação.


---
## Testes

Na pasta modelo, desse repositório, se encontra o arquivo de teste do modelo `test_modelo.py`

Utilizando a ferramenta `pytest`,  é possível realizar um teste unitário no modelo exportado. A condições para sucesso dos teste é a obtenção de acurária e precisão acima de 80%, para o conjunto de teste.

Para executar o teste, navegue até o diretório onde se encontra o arquivo `test_modelo.py` e execute o comando `pytest -v`
