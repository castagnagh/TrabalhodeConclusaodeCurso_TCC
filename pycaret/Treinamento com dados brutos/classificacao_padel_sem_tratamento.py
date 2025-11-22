
# %%
##           1
##############################
import pandas as pd
from pycaret.classification import *

df = pd.read_excel("Pasta1.xlsx")
df = df.dropna(subset=["AUTOAVALIACAO : CATEGORIA"])
print(df.columns)

# %%
##           2
##############################
exp = setup(
    data=df,
    target="AUTOAVALIACAO : CATEGORIA",
    session_id=123,
    normalize=True,
    train_size=0.8,
    ignore_features = ["DADOS_PESSOAIS : NOME"]# ignora nome
)

# %%
##           3
##############################
best_model = compare_models()

# %%
##           4
##############################
tuned_model = tune_model(best_model)

# %%
##           5
##############################
dados_tratados = predict_model(tuned_model, data=df)
dados_tratados.to_excel("DadosTratados.xlsx", index=False)

# %%
##           6
##############################
#dados não tratados em texto
new_data = pd.read_excel("NovosAtletas.xlsx")
predicoes = predict_model(tuned_model, data=new_data)
predicoes.to_excel("Previsoes_NovosAtletas_texto.xlsx", index=False)

# %%
##           7
##############################
pd.set_option('display.max_rows', None)

comparacao = predict_model(tuned_model, data=df)

comparacao['Resultado'] = [
    'ACERTOU' if v == p else 'ERROU' 
    for v, p in zip(comparacao['AUTOAVALIACAO : CATEGORIA'], comparacao['prediction_label'])
]

print("=== Comparação Acertos/Erros (primeiras 10 linhas) ===")
print(comparacao[['AUTOAVALIACAO : CATEGORIA', 'prediction_label', 'Resultado']])

# Mostrar resumo de acertos e erros
resumo = comparacao['Resultado'].value_counts()
print("\n=== Resumo Geral ===")
print(resumo)

# Mostrar resumo por categoria real
resumo_categoria = comparacao.groupby(['AUTOAVALIACAO : CATEGORIA', 'prediction_label']).size().unstack(fill_value=0)
print("\n=== Resumo por Categoria ===")
print(resumo_categoria)


# %%
from pycaret.classification import save_model

save_model(tuned_model, 'modelo_padel')

# %%
