from pydantic import BaseModel
from typing import Optional, List
from model.paciente import Paciente

# import json
# import numpy as np


class PacienteSchema(BaseModel):
    """Define como um novo paciente a ser inserido deve ser representado"""

    age: int = 49
    sex: str = "F"
    shestpaintype: str = "NAP"
    restingbp: int = 160
    cholesterol: int = 180
    fastingbs: int = 0
    restingecg: str = "Normal"
    maxhr: float = 156
    exerciseangina: str = "N"
    oldpeak: float = 1
    st_slope: str = "Flat"


class PacienteViewSchema(BaseModel):
    """Define como um paciente será retornado"""

    id: int = 1
    age: int = 49
    sex: str = "F"
    shestpaintype: str = "NAP"
    restingbp: int = 160
    cholesterol: int = 180
    fastingbs: int = 0
    restingecg: str = "Normal"
    maxhr: float = 156
    exerciseangina: str = "N"
    oldpeak: float = 1
    st_slope: str = "Flat"
    outcome: Optional[int] = None


class PacienteBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do paciente.
    """

    id: int = 1


class PacienteDiagnosticoSchema(BaseModel):
    """Devine como é o retorno da informação do diagnóstico de um paciente."""

    diagnostico: int = 1


class ListaPacientesSchema(BaseModel):
    """Define como uma lista de pacientes será representada"""

    pacientes: List[PacienteSchema]


class PacienteDelSchema(BaseModel):
    """Define como um paciente para deleção será representado"""

    id: int = 1


# Apresenta apenas os dados de um paciente
def apresenta_paciente(paciente: Paciente):
    """Retorna uma representação do paciente seguindo o schema definido em
    PacienteViewSchema.
    """
    return {
        "id": paciente.id,
        "age": paciente.age,
        "sex": paciente.sex,
        "shestpaintype": paciente.shestpaintype,
        "restingbp": paciente.restingbp,
        "cholesterol": paciente.cholesterol,
        "fastingbs": paciente.fastingbs,
        "restingecg": paciente.restingecg,
        "maxhr": paciente.maxhr,
        "exerciseangina": paciente.exerciseangina,
        "oldpeak": paciente.oldpeak,
        "st_slope": paciente.st_slope,
        "diagnostico": paciente.diagnostico,
    }


# Apresenta uma lista de pacientes
def apresenta_pacientes(pacientes: List[Paciente]):
    """Retorna uma representação do paciente seguindo o schema definido em
    PacienteViewSchema.
    """
    result = []
    for paciente in pacientes:
        result.append(
            {
                "id": paciente.id,
                "age": paciente.age,
                "sex": paciente.sex,
                "shestpaintype": paciente.shestpaintype,
                "restingbp": paciente.restingbp,
                "cholesterol": paciente.cholesterol,
                "fastingbs": paciente.fastingbs,
                "restingecg": paciente.restingecg,
                "maxhr": paciente.maxhr,
                "exerciseangina": paciente.exerciseangina,
                "oldpeak": paciente.oldpeak,
                "st_slope": paciente.st_slope,
                "diagnostico": paciente.diagnostico,
            }
        )

    return {"pacientes": result}
