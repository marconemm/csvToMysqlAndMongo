import pandas as pd

# Carregar o arquivo CSV para um DataFrame
df = pd.read_csv('netflix_titles.csv', encoding='latin1')

# Lista para armazenar os DataFrames normalizados
normalized_dfs = []

# Normalizar colunas com mais de um valor por linha
for col in df.columns:
    # Converter a coluna para o tipo string
    df[col] = df[col].astype(str)
    # Dividir a coluna em várias colunas
    split_cols = df[col].str.split(',').apply(pd.Series)
    # Renomear as novas colunas
    split_cols = split_cols.rename(columns=lambda x: f'{col}_{x}')
    # Adicionar os novos DataFrames à lista
    normalized_dfs.append(split_cols)

# Concatenar todos os DataFrames normalizados
result_df = pd.concat(normalized_dfs, axis=1)

#Salvar o DataFrame normalizado em um novo arquivo CSV
result_df.to_csv('arquivo_normalizado.csv', index=False)
