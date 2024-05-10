import pandas as pd
from utils import UTF8

# Função para capitalizar apenas se o valor for uma string:
def capitalizar_string(valor):
    if isinstance(valor, str):
        return valor.title()
    
    return valor

def trata_data_frame(path: str) -> pd.DataFrame:
    """Trata um respectivo data frame, removendo colunas valizas, a coluna "show_id" e preenche as células vazias com "null".

    Args:
        path (str): Caminho relativo para o CSV que será analizado.

    Returns:
        pd.DataFrame: Data frame tratado.
    """
    df = pd.read_csv(path, encoding=UTF8)

    # Remove colunas vazias:
    df.drop(
        df.columns[df.columns.str.contains("Unnamed", case=False)], axis=1, inplace=True
    )

    # Remove coluna "show_id":
    if "show_id" in df.columns:
        df.drop("show_id", axis=1, inplace=True)

    # Aplicando a função title() para deixar todas as iniciais maiúsculas:
    for coluna in df.columns:
        df[coluna] = df[coluna].apply(capitalizar_string)

    # Troca todos as células vazias por "null":
    df = df.fillna("null")

    return df


def salva_valores_unicos(df: pd.DataFrame, save_in: dict, excecao: tuple) -> None:
    """Salva os valores únicos de cada coluna analizada.

    Args:
        df (pd.DataFrame): Dataframe que será analizado.
        save_in (dict): Variável na qual os dados únicos serão registrados.
        excecao (tuple): Uma coleção com os nomes das colunas que estão multi-valoradas. 
    """
    for coluna in df.columns:  # Descobre os valores únicos de cada coluna:
        print(f'Analizando a coluna "{coluna}"...\n')
        unicos_set = set({})
        valores_unicos = df[coluna].unique()

        for (
            valor_unico
        ) in valores_unicos:  # Analiza de cada um dos valores únicos está multivalorado:
            if valor_unico == "null":
                continue

            valor_unico = str(valor_unico).strip()

            if (coluna not in excecao) and ("," in valor_unico):
                valores = str(valor_unico).split(",")

                for valor in valores:
                    valor = valor.strip()
                    unicos_set.add(valor)

            else:
                unicos_set.add(valor_unico)

        save_in[coluna] = unicos_set

    print("Valores únicos obtidos com sucesso.\n")


def cria_sub_dicionario(path: str, fonte: dict) -> dict:
    """Criar sub dicionarios, baseando-se em arquivos CSV para tal.

    Args:
        path (str): Caminho relativo para o CSV que será analizado.
        fonte (dict): Dicionario com os valores únicos.

    Returns:
        dict: Dicionário com todos os valores unicos tratados.
    """
    chaves_desejadas = trata_data_frame(path).columns

    result = {chave: fonte[chave] for chave in chaves_desejadas}

    print(f'\n--\nCriado um Dicionário, conforme os títulos do CSV: "{path}"\n')
    print(result)
    print("\n--")

    return result
