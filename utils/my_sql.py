import mysql.connector
import os
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
from dotenv import load_dotenv
from utils.funcoes import cria_sub_dicionario, read_csv_to_dict
from utils import EXCEPT_FILL_DB_BY_CSV


def conect_to_db() -> PooledMySQLConnection | MySQLConnectionAbstract:
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
    values = columns = ""
    script = f"INSERT INTO `{nome_tabela}` "

    for i, coluna in enumerate(tuple(fonte.keys())):
        if i == 0:
            columns += f"(`{coluna}"

        elif i == len(fonte.keys()) - 1:
            columns += f"`, `{coluna}"

        else:
            columns += f"`, `{coluna}"

    columns += "`)"
    script += f"{columns} VALUES "

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
    table_name = path.split(separator)[2]
    table_name = table_name[0 : len(table_name) - 4]
    table_name = table_name + "_tbl"
    data = cria_sub_dicionario(path, fonte)
    sql = cria_script_sql(data, table_name)
    erros = {}

    with conect_to_db() as conn:
        with conn.cursor() as cursor:
            for column in data:
                erros[column] = []

                for value in data[column]:
                    try:
                        values_tuple = tuple([value])

                        cursor.execute(sql, values_tuple)

                        print(
                            f'Valor "{value}", inserido na tabela "{table_name}" com sucesso!\n'
                        )

                    except mysql.connector.Error as msce:
                        erros[column].append({msce.errno: msce.msg})

            if erros[column]:
                print(f"ERROS:\n")
                for column in erros.keys():
                    for erro in erros[column]:
                        for key in erro.keys():
                            print(
                                f'tabela "{table_name}", coluna "{column}": erro {key} -> {erro[key]}'
                            )

                conn.rollback()

                raise RuntimeError(
                    "Ocorreu um erro durante a inserção no banco de dados."
                )

            else:
                conn.commit()


def insert_uniques_into_db(csv_paths_tuple: tuple, data: dict) -> None:
    """Insere os dados únicos em todas as tabelas de coluna única."""
    for csv_path in csv_paths_tuple:
        csv_path = f"database/{csv_path}"

        insert_unique_into_db(csv_path, data)


def find_id(query: str, value: str) -> int | None:
    """Find an id on database.

    Args:
        query (str): the SQL  query to execute the seek.
        value (str): the value to fill the SQL  query.

    Raises:
        RuntimeError: In case of some SGBD error.

    Returns:
        int: the found id, or None if the seek returns no value.
    """
    value = tuple([value])

    try:
        with conect_to_db() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, value)
                response = cursor.fetchone()

            if response:
                return int(response["id"])

            return None

    except mysql.connector.Error as msce:
        raise RuntimeError("Erro ao buscar o ID:", msce)


def insert_into_show_tbl(csv_path: str) -> None:
    data = read_csv_to_dict(csv_path, EXCEPT_FILL_DB_BY_CSV)

    with conect_to_db() as conn:
        with conn.cursor() as cursor:
            for row in data.values():
                INSERT_QUERY = "INSERT INTO `show_tbl` (title, date_added, release_year, duration, description, type_id, rating_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"

                try:
                    TYPE_ID = find_id(
                        "SELECT id FROM `type_tbl` WHERE type = %s", row["type"]
                    )

                    RATING_ID = find_id(
                        "SELECT id FROM `rating_tbl` WHERE rating = %s", row["rating"]
                    )

                    values = (
                        row["title"],
                        row["date_added"],
                        row["release_year"],
                        row["duration"],
                        row["description"],
                        TYPE_ID,
                        RATING_ID,
                    )

                    cursor.execute(INSERT_QUERY, values)

                    print('Dado inserido com sucesso na tabela "show_tbl"!\n')

                except mysql.connector.Error as msce:
                    raise RuntimeError("Erro ao buscar o ID:", msce)

            conn.commit()
