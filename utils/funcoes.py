import pandas as pd


def trata_data_frame(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf_8")

    # Remove colunas vazias:
    df.drop(
        df.columns[df.columns.str.contains("Unnamed", case=False)], axis=1, inplace=True
    )

    # Remove coluna "show_id":
    if "show_id" in df.columns:
        df.drop("show_id", axis=1, inplace=True)

    # Troca todos as células vazias por "null":
    df = df.fillna("null")

    return df


def salva_valores_unicos(df: pd.DataFrame, save_in: dict, excecao: list) -> None:
    for coluna in df.columns:  # Descobre os valores únicos de cada coluna:
        print(f'Analizando a coluna "{coluna}"...\n')
        unicos_set = set({})
        unicos = df[coluna].unique()

        for (
            unico
        ) in unicos:  # Analiza de cada um dos valores únicos está multivalorado:
            if unico == "null":
                continue

            unico = str(unico).strip()

            if (coluna not in excecao) and ("," in unico):
                valores = str(unico).split(",")

                for valor in valores:
                    valor = valor.strip()
                    unicos_set.add(valor)

            else:
                unicos_set.add(unico)

        save_in[coluna] = unicos_set

    print("Valores únicos obtidos com sucesso.\n")


def cria_sub_dict(path: str, fonte: dict) -> dict:
    chaves_desejadas = trata_data_frame(path).columns

    result = {chave: fonte[chave] for chave in chaves_desejadas}

    print(f'\n--\nCriado o sub_dict, conforme os títulos do CSV: "{path}"\n')
    print(result)
    print("\n--")

    return result
