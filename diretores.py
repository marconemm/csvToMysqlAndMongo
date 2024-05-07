import pandas as pd

def normaliza_diretores() -> None:
    # Ler o arquivo CSV
    df = pd.read_csv('arquivo_normalizado.csv', low_memory=False)

    # Selecionar todas as colunas relacionadas a diretores
    diretor_columns = [col for col in df.columns if 'director' in col.lower()]

    # Combinar todas as colunas de diretores em uma única coluna
    df['director'] = df[diretor_columns].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)

    # Remover as colunas de diretores originais
    df.drop(diretor_columns, axis=1, inplace=True)

    # Dividir os diretores em linhas separadas
    df = df.assign(director=df['director'].str.split(', ')).explode('director')

    # Remover linhas vazias
    df = df.dropna(subset=['director'])

    # Resetar os índices
    df.reset_index(drop=True, inplace=True)

    # Salvar os diretores em um novo arquivo CSV
    df['director'].to_csv('diretores.csv', index=False, header=['director'])

def tira_espacos_em_branco_de_diretores() -> None:
    # Ler o arquivo CSV
    df = pd.read_csv('diretores.csv')

    # Remover linhas vazias da coluna 'director'
    df = df.dropna(subset=['director'])

    # Resetar os índices
    df.reset_index(drop=True, inplace=True)

    # Salvar o DataFrame resultante em um novo arquivo CSV
    df.to_csv('diretores_sem_vazios.csv', index=False)

tira_espacos_em_branco_de_diretores();