from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

# colunas = Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope, HeartDisease


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True)

    age = Column("Age", Integer, nullable=False)
    sex = Column("Sex", String(1), nullable=False)
    shestpaintype = Column("ChestPainType", String(3), nullable=False)
    restingbp = Column("RestingBP", Integer, nullable=False)
    cholesterol = Column("Cholesterol", Integer, nullable=False)
    fastingbs = Column("FastingBS", Integer, nullable=False)
    restingecg = Column("RestingECG", String(10), nullable=False)
    maxhr = Column("MaxHR", Float, nullable=False)
    exerciseangina = Column("ExerciseAngina", String(1), nullable=False)
    oldpeak = Column("Oldpeak", Float, nullable=False)
    st_slope = Column("ST_Slope", String(10), nullable=False)

    diagnostico = Column("Diagnostic", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(
        self,
        age: int,
        sex: String,
        shestpaintype: String,
        restingbp: int,
        cholesterol: int,
        fastingbs: int,
        restingecg: String,
        maxhr: float,
        exerciseangina: String,
        oldpeak: float,
        st_slope: String,
        diagnostico: int,
        data_insercao: Union[DateTime, None] = None,
    ):
        """
        Cria um Paciente

        age: idade do paciente [anos]
        sex: sexo do paciente [M: masculino ou F: feminino]
        shestpaintype: tipo de dor torácica [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic]
        restingbp: pressão arterial em repouso [mm Hg]
        cholesterol: Colesterol Sérico [mm/dl]
        fastingbs: Glicemia em Jejum [1: if FastingBS > 120 mg/dl, 0: otherwise]
        restingecg: Resultados do Eletrocardiograma em Repouso [Normal: Normal, ST: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV), LVH: showing probable or definite left ventricular hypertrophy by Estes' criteria]
        maxhr: Frequência Cardíaca Máxima Alcançada [valor numérico entre 60 e 202]
        exerciseangina: Angina Induzida por Exercício [Y: Yes, N: No]
        oldpeak: Oldpeak ST ST [Valor numérico medido na depressão]
        st_slope Inclinação do Segmento ST do Pico do Exercício [Up: upsloping, Flat: flat, Down: downsloping]

        diagnostico: diagnóstico
        data_insercao: data de quando o paciente foi inserido à base


        """
        self.age = age
        self.sex = sex
        self.shestpaintype = shestpaintype
        self.restingbp = restingbp
        self.cholesterol = cholesterol
        self.fastingbs = fastingbs
        self.restingecg = restingecg
        self.maxhr = maxhr
        self.exerciseangina = exerciseangina
        self.oldpeak = oldpeak
        self.st_slope = st_slope
        self.diagnostico = diagnostico

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
