import csv, unicodedata, pandas as pd
from utils import UTF8
from datetime import datetime


def iniciais_maiusculas(valor: any) -> any:
    """Deixa todas as iniciais de valores tipo texto em maiúscula.
    Args:
        valor (any): o valor que será tratado.

    Returns:
        any: valor tratado, caso seja do tipo texto.
    """
    if isinstance(valor, str):
        valor = valor.lower()
        
        return valor.title()

    return valor


def remover_acentos(valor: any) -> any:
    """Remove a acentuação do texto.

    Args:
        valor (any): texto que será tratado

    Returns:
        any: texto sem a acentuação
    """
    if isinstance(valor, str):
        return "".join(
            letra
            for letra in unicodedata.normalize("NFD", valor)
            if unicodedata.category(letra) != "Mn"
        )

    return valor


def trata_data_frame(path: str, excecao: tuple = ()) -> pd.DataFrame:
    """Trata um respectivo data frame, removendo colunas valizas, a coluna "show_id" e preenche as células vazias com "null".

    Args:
        path (str): Caminho relativo para o CSV que será analizado.
        excecao (tuple, optional): uma coleção com as colunas que não receberão as iniciais maiúsculas. Padrão: ().

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

    for coluna in df.columns:
        # formatando dados textuais:
        df[coluna] = df[coluna].apply(remover_acentos)

        if coluna not in excecao:
            df[coluna] = df[coluna].apply(iniciais_maiusculas)

    # Troca todos as células vazias por "null":
    df = df.fillna("null")

    return df


def salva_valores_unicos(df: pd.DataFrame, excecao: tuple = ()) -> dict:
    """Retorna os valores únicos de cada coluna analizada.

    Args:
        df (pd.DataFrame): dataframe que será analizado.
        excecao (tuple, optional): uma coleção com os nomes das colunas que estão multi-valoradas. Padrão: ().

    Returns:
        dict: dicionário com os respectivos valores unicos do dataframe analizado.
    """
    result = {}

    for coluna in df.columns:  # Descobre os valores únicos de cada coluna:
        print(f'Analizando a coluna "{coluna}"...\n')
        unicos_set = set({})
        valores_unicos = df[coluna].unique()

        for (
            valor_unico
        ) in (
            valores_unicos
        ):  # Analiza de cada um dos valores únicos está multivalorado:
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

        result[coluna] = unicos_set

    print("Valores únicos obtidos com sucesso.\n")

    return result


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


def read_csv_to_dict(csv_file: str, excecao: tuple = ()) -> dict:
    """Ler um CSV e retorna seus valores em um dicionário.

    Args:
        csv_file (str): caminho relativo para o *.csv
        excecao (tuple, optional): tupla com os valores de colunas que não receberão formatação de dados. Padrão: ().

    Returns:
        dict: dicionário contendo todas as linhas do *.csv
    """
    data_dict = {}

    with open(csv_file, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        for i, row in enumerate(csv_reader):
            data_dict[i + 1] = {}

            for key, value in row.items():
                if value:
                    if key not in excecao:
                        data_dict[i + 1].update({key: value.title().strip()})

                    elif key == "release_year":
                        data_dict[i + 1].update({key: int(value)})

                    elif key == "date_added":
                        value = str(value).strip()
                        data_dict[i + 1].update(
                            {key: datetime.strptime(value, "%B %d, %Y")}
                        )

                    else:
                        data_dict[i + 1].update({key: value.strip()})
                else:
                    data_dict[i + 1].update({key: None})

    return data_dict
