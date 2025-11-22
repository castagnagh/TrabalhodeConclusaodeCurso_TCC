
# %%
##           1
##############################
import pandas as pd
from pycaret.classification import *

df = pd.read_excel("planilha_numeros.xlsx")
df = df.dropna(subset=["AUTOAVALIACAO: CATEGORIA"])

# %%
##           2
##############################
colunas_likert = [
    "COMPOSICAO_JOGO: SAQUE",
    "COMPOSICAO_JOGO: USA_RETOQUE",
    "COMPOSICAO_JOGO: VOLEIO_ATAQUE",
    "COMPOSICAO_JOGO: VOLEIO_DEFESA_CONTENSAO",
    "COMPOSICAO_JOGO: BANDEJA_RETOMADA_REDE",
    "COMPOSICAO_JOGO: SMASH",
    "COMPOSICAO_JOGO: TROCA_BOLA_FUNDO_FOREHAND",
    "COMPOSICAO_JOGO: TROCA_BOLA_FUNDO_BACKHAND",
    "COMPOSICAO_JOGO: DEVOLUCAO_SAQUE",
    "COMPOSICAO_JOGO: SAIDA_PAREDE_DEFESA",
    "COMPOSICAO_JOGO: SAIDA_PAREDE_ATAQUE",
    "COMPOSICAO_JOGO: MOVIMENTACAO",
    "COMPOSICAO_JOGO: POSICIONAMENTO",
    "HABILIDADE_TECNICA: MOVIMENTACAO"
]

colunas_ordinais = [
    "DADOS_PESSOAIS: FAIXA_ETARIA",
    "EXPERIENCIA: TEMPO_PADEL",
    "EXPERIENCIA: QUANTIDADE_TREINOS",
    "EXPERIENCIA: QUANTIDADE_JOGOS",
    "EXPERIENCIA: CATEGORIA_EM_TORNEIOS",
    "DADOS_PESSOAIS: POSICAO_QUADRA",
    "COMPOSICAO_JOGO: DEFESA_ATAQUE",
    "COMPOSICAO_JOGO: CONTROLE_RITMO",
    "OBJETIVO: ESTILO_DUPLAS",
    "EXPERIENCIA: PARTICIPA_TORNEIOS",
]

# %%
##           3
##############################
# Converter ordinais para categoria
for col in colunas_ordinais:
    df[col] = df[col].astype("category")


# %%
##           4
##############################
exp = setup(
    data=df,
    target="AUTOAVALIACAO: CATEGORIA",
    session_id=123,
    normalize=True,
    train_size=0.8,
    categorical_features=colunas_ordinais,   # força PyCaret a tratar essas como categóricas
    numeric_features=colunas_likert,          # garante que Likert são numéricas
    ignore_features=["DADOS_PESSOAIS: NOME"] # ignora nome
)

# %%
##           5
##############################
best_model = compare_models()

# %%
##           6
##############################
tuned_model = tune_model(best_model)

# %%
##           7
##############################
dados_tratados = predict_model(tuned_model, data=df)
dados_tratados.to_excel("DadosTratados.xlsx", index=False)

# %%
##           8
##############################
##dados tratados em forma de Numeros
new_data = pd.read_excel("NovosAtletas_num.xlsx")
predicoes = predict_model(tuned_model, data=new_data)
predicoes.to_excel("Previsoes_NovosAtletas.xlsx", index=False)

# %%
##           9
##############################

    # "iniciante": 1,
    # "7ª categoria": 2,
    # "6ª categoria": 3,
    # "5ª categoria": 4,
    # "4ª categoria": 5,
    # "3ª categoria": 6,
    # "2ª categoria": 7,
    # "1ª categoria": 8

pd.set_option('display.max_rows', None)

comparacao = predict_model(tuned_model, data=df)

comparacao['Resultado'] = [
    'ACERTOU' if v == p else 'ERROU' 
    for v, p in zip(comparacao['AUTOAVALIACAO: CATEGORIA'], comparacao['prediction_label'])
]

print("=== Comparação Acertos/Erros (primeiras 10 linhas) ===")
print(comparacao[['AUTOAVALIACAO: CATEGORIA', 'prediction_label', 'Resultado']])

# Mostrar resumo de acertos e erros
resumo = comparacao['Resultado'].value_counts()
print("\n=== Resumo Geral ===")
print(resumo)

# Mostrar resumo por categoria real
resumo_categoria = comparacao.groupby(['AUTOAVALIACAO: CATEGORIA', 'prediction_label']).size().unstack(fill_value=0)
print("\n=== Resumo por Categoria ===")
print(resumo_categoria)


# %%
