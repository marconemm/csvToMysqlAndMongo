import mysql.connector
import os
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
from dotenv import load_dotenv
from utils.funcoes import cria_sub_dicionario


def conectar_db() -> PooledMySQLConnection | MySQLConnectionAbstract:
    """Conecta com o banco de dados.

    Returns:
        PooledMySQLConnection | MySQLConnectionAbstract: instancia da conexão com o banco de dados.
    """
    load_dotenv()

    return mysql.connector.connect(
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        database=os.getenv("DATABASE_NAME"),
    )


def cria_script_sql(fonte: dict, nome_tabela: str) -> str:
    # "INSERT INTO type_tbl (type) VALUES (%s)"
    values = colunas = ""
    script = f"INSERT INTO `{nome_tabela}` "

    for i, coluna in enumerate(tuple(fonte.keys())):
        if i == 0:
            colunas += f"(`{coluna}"

        elif i == len(fonte.keys()) - 1:
            colunas += f"`, `{coluna}"

        else:
            colunas += f"`, `{coluna}"

    colunas += "`)"
    script += f"{colunas} VALUES "

    for i in range(len(fonte)):
        if i == 0:
            values += "(%s"

        elif i == len(fonte) - 1:
            values += " %s"

        else:
            values += " %s,"

    script += f"{values});"

    return script


def insert_unique_into_db(path: str, fonte: dict) -> None:
    """Executar um script no banco de dados.

    Args:
        script (str): Script que será executado.
    """
    separator = "\\" if os.name == "nt" else "/"
    nome_tabela = path.split(separator)[2]
    nome_tabela = nome_tabela[0 : len(nome_tabela) - 4]
    nome_tabela = nome_tabela + "_tbl"
    dados = cria_sub_dicionario(path, fonte)
    sql = cria_script_sql(dados, nome_tabela)
    erros = {}

    with conectar_db() as conexao:
        with conexao.cursor() as cursor:
            for coluna in dados:
                erros[coluna] = []

                for valor in dados[coluna]:
                    try:
                        valores = [valor]
                        valores = tuple(valores)

                        cursor.execute(sql, valores)

                        print(
                            f'Valor "{valor}", inserido na tabela "{nome_tabela}" com sucesso!\n'
                        )

                    except mysql.connector.Error as mqce:
                        erros[coluna].append({mqce.errno: mqce.msg})

            if erros[coluna]:
                print(f"ERROS:\n")
                for coluna in erros.keys():
                    for erro in erros[coluna]:
                        for key in erro.keys():
                            print(
                                f'tabela "{nome_tabela}", coluna "{coluna}": erro {key} -> {erro[key]}'
                            )

                conexao.rollback()
                
                raise RuntimeError(
                    "Ocorreu um erro durante a inserção no banco de dados."
                )

            else:
                conexao.commit()


def insert_uniques_into_db(paths_tuple: tuple, dados: dict) -> None:
    """Insere os dados únicos em todas as tabelas de coluna única."""
    for csv in paths_tuple:
        csv = f"database/{csv}"
        if "show" in csv:
            pass
        else:
            insert_unique_into_db(csv, dados)
