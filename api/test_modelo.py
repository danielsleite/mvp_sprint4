# Arquivo de teste para validar a performance do modelo
from model.modelo import Model
from model.avalidaor import Avaliador

# from sklearn.ensemble import GradientBoostingClassifier

# # from api.model import avalidaor


def test_modelo():
    ml_path = "./ml_model/classificador.pkl"
    scaler_path = "./ml_model/scaler.pkl"
    dict_path = "./ml_model/dicionario.pkl"
    X_test_path = "./ml_model/x_test.pkl"
    y_test_path = "./ml_model/y_test.pkl"

    avaliador = Avaliador()

    model = Model(model_path=ml_path, scaler_path=scaler_path, dict_path=dict_path)
    X_test = model.carrega_modelo(X_test_path)
    y_test = model.carrega_modelo(y_test_path)
    scaler = model.carrega_modelo(scaler_path)

    # Como o dado de test da base já foi exportado com as transformações de label, será
    # necessário apenas reescalonar os dados

    x_scaler = scaler.transform(X_test)

    # Obtendo as métricas
    acuracia, recall, precisao, f1 = avaliador.avaliar(model, x_scaler, y_test)
    msg = f"acuracia: {acuracia}, recall: {recall}, precisao: {precisao}, f1: {f1}"
    print(msg)

    # Condições de sucesso do tsete
    assert acuracia >= 0.80
    assert precisao >= 0.80
