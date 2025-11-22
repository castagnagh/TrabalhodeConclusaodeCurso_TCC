import pandas as pd
from django.conf import settings
import os
from pycaret.classification import load_model, predict_model

BASE_DIR = settings.BASE_DIR

class PredictionEngine:
    # Caminho absoluto para o modelo treinado
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "repadel", "ml_models", "modelo_padel")

    # Carrega uma única vez (PyCaret exige SEM extensão .pkl)
    modelo = load_model(MODEL_PATH)

    @staticmethod
    def prever_categoria(respostas_dict):
        """
        Recebe um dicionário EXATAMENTE no padrão do XLSX e retorna a categoria prevista.

        Exemplo esperado:
        {
            "DADOS_PESSOAIS: SEXO": "Feminino",
            "DADOS_PESSOAIS: FAIXA_ETARIA": "Entre 36 e 45 anos",
            "DADOS_PESSOAIS: POSICAO_QUADRA": "Direita"
        }
        """

        # Converte para DataFrame (PyCaret exige isso)
        df = pd.DataFrame([respostas_dict])

        # Realiza previsão
        resultado = predict_model(PredictionEngine.modelo, data=df)

        # Resultado principal
        predicao = resultado["prediction_label"].iloc[0]

        # Probabilidades
        probas = (
            resultado.filter(like="prediction_score")
                     .iloc[0]
                     .to_dict()
        )

        return {
            "categoria_prevista": predicao,
            "detalhes": probas
        }
