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


def inicia_script_sql(fonte: dict, nome_tabela: str) -> str:
    # "INSERT INTO type_tbl (type) VALUES (%s)"
    values = "("
    colunas = "(`"

    for coluna in tuple(fonte.keys()):
        colunas += coluna
        colunas += "`"

    script = f"INSERT INTO `{nome_tabela}` "
    script += colunas
    script += ") VALUES "

    for i in range(len(fonte)):
        if i == 0:
            values += "%s"
        elif i == len(fonte) - 1:
            values += " %s"
        else:
            values += ", %s,"

    script += values + ");"

    return script


def executar_script_sql(path: str, fonte: dict) -> None:
    """Executar um script no banco de dados.

    Args:
        script (str): Script que será executado.
    """
    separator = "\\" if os.name == "nt" else "/"
    nome_tabela = path.split(separator)[2]
    nome_tabela = nome_tabela[0 : len(nome_tabela) - 4]
    nome_tabela = nome_tabela + "_tbl"
    dados = cria_sub_dicionario(path, fonte)

    with conectar_db() as conexao:
        with conexao.cursor() as cursor:
            for coluna in dados:
                for valor in dados[coluna]:
                    try:
                        # sql = "INSERT INTO tabela (coluna) VALUES (valor);"
                        sql = inicia_script_sql(dados, nome_tabela)
                        valores = [valor]
                        valores = tuple(valores)

                        cursor.execute(sql, valores)
                        conexao.commit()

                        print(
                            f'Valor "{valor}", inserido na tabela "{nome_tabela}" com sucesso!'
                        )

                    except mysql.connector.Error as mqce:
                        raise RuntimeError(mqce.msg)
