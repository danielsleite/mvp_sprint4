import numpy as np
import pickle
import joblib

from logger import logger


class Model:
    def __init__(self, model_path: str, scaler_path: str, dict_path: str):
        self.modelo = self.carrega_modelo(model_path)
        self.scaler = self.carrega_modelo(scaler_path)
        self.dicionario = self.carrega_modelo(dict_path)
        print(self.dicionario)

    def carrega_modelo(self, path):
        """Dependendo se o final for .pkl ou .joblib, carregamos de uma forma ou de outra"""

        if path.endswith(".pkl"):
            temp = pickle.load(open(path, "rb"))
        elif path.endswith(".joblib"):
            temp = joblib.load(path)
        else:
            raise Exception("Formato de arquivo não suportado")
        logger.warning(path)
        return temp

    def preditor(self, form):
        """Realiza a predição de um paciente com base no modelo treinado

        Os dados no formato de label, são transformados em dados numéricos com base
        no dicionário exportado
        """
        x_input = np.array(
            [
                form.age,  # age of the patient [years]
                self.dicionario[form.sex],  # sex of the patient [M: Male, F: Female]
                self.dicionario[
                    form.shestpaintype
                ],  # chest pain type [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic]
                form.restingbp,  # resting blood pressure [mm Hg]
                form.cholesterol,  # serum cholesterol [mm/dl]
                form.fastingbs,  # fasting blood sugar [1: if FastingBS > 120 mg/dl, 0: otherwise]
                self.dicionario[
                    form.restingecg
                ],  # resting electrocardiogram results [Normal: Normal, ST: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV), LVH: showing probable or definite left ventricular hypertrophy by Estes' criteria]
                form.maxhr,  # maximum heart rate achieved [Numeric value between 60 and 202]
                self.dicionario[
                    form.exerciseangina
                ],  # exercise-induced angina [Y: Yes, N: No]
                form.oldpeak,  # oldpeak = ST [Numeric value measured in depression]
                self.dicionario[
                    form.st_slope
                ],  # the slope of the peak exercise ST segment [Up: upsloping, Flat: flat, Down: downsloping]
            ]
        )
        # Faremos o reshape para que o modelo entenda que estamos passando

        msg = f"Entrada de dados: {x_input}"
        logger.warning(msg)
        x_input = x_input.reshape(1, -1)
        msg = f"Reshape entrada de dados: {x_input}"
        logger.warning(msg)
        x_input_scaler = self.scaler.transform(x_input)
        msg = f"Dado transforamdo: {x_input_scaler}"
        logger.warning(msg)
        diagnosis = self.modelo.predict(x_input_scaler)
        msg = f" Resultado do diagnóstico: {diagnosis[0]}"
        logger.warning(msg)
        return int(diagnosis[0])

    def predict(self, x_input):
        return self.modelo.predict(x_input)
