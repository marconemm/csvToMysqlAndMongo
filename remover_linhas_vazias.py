import pandas as pd

# Ler o arquivo CSV
df = pd.read_csv('database/netflix_titles.csv', encoding='latin1')

def remover_linhas_vazias(nome_coluna:str) -> None:
    # Remover linhas vazias da coluna 'cast'
    df2 = df.dropna(subset=[nome_coluna])

    # Dividir os valores da coluna 'cast' em múltiplas linhas
    cast_series = df2['cast'].str.split(',').explode().str.strip()

    # Criar um novo DataFrame com a coluna 'cast' isolada
    novo_df = pd.DataFrame({f'{nome_coluna}': cast_series})

    # Salvar o novo DataFrame em um novo arquivo SV
    novo_df.to_csv(f'database/sem_espacos/{nome_coluna}_sem_vazios.csv', index=False)

colunas = df.columns
    
for coluna in colunas:
    if "Unnamed" not in coluna:
        remover_linhas_vazias(coluna)

