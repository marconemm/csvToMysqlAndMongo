import mysql.connector
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
from utils.funcoes import cria_sub_dicionario, read_csv_to_dict
from utils import EXCEPT_FILL_DB_BY_CSV, SOURECES_TABLES
from models.Show import Show


def conect_to_db() -> PooledMySQLConnection | MySQLConnectionAbstract:
    """Conecta com o banco de dados.

    Returns:
        PooledMySQLConnection | MySQLConnectionAbstract: instancia da conexão com o banco de dados.
    """
    import os
    from dotenv import load_dotenv

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


def insert_into_source_tbl(path: str, fonte: dict) -> None:
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


def insert_into_sources_tbl_by_csv(csv_paths_tuple: tuple, data: dict) -> None:
    """Insere os dados únicos em todas as tabelas de coluna única."""
    for csv_path in csv_paths_tuple:
        csv_path = f"database/{csv_path}"

        insert_into_source_tbl(csv_path, data)


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

                # Iterar sobre os resultados restantes e descartá-los
                for _ in cursor:
                    pass

            if response:
                return int(response["id"])

            return None

    except mysql.connector.Error as msce:
        raise RuntimeError("Erro ao buscar o ID:", msce)


def mysql_select_show_by_id(id: int) -> Show:
    show = Show()
    VALUES = tuple([id])

    try:
        with conect_to_db() as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = """SELECT s.id, s.title, s.release_year, s.date_added, s.description, s.duration, t.type, r.rating FROM projeto_database_db.show_tbl AS s INNER JOIN projeto_database_db.type_tbl AS t ON s.type_id = t.id INNER JOIN projeto_database_db.rating_tbl AS r ON s.rating_id = r.id WHERE s.id = %s;"""
                cursor.execute(query, VALUES)
                response = cursor.fetchall()

                if response:
                    show.set_show_attr(response)

                    query = """SELECT d.director FROM projeto_database_db.show_tbl AS s INNER JOIN projeto_database_db.show_director_tbl AS sd ON s.id = sd.id_show INNER JOIN projeto_database_db.director_tbl AS d ON sd.id_director = d.id WHERE s.id = %s;"""
                    cursor.execute(query, VALUES)
                    show.set_director_list(cursor.fetchall())

                    query = """SELECT c.country FROM projeto_database_db.show_tbl AS s INNER JOIN projeto_database_db.show_country_tbl AS sc ON s.id = sc.id_show INNER JOIN projeto_database_db.country_tbl AS c ON c.id = sc.id_country WHERE s.id = %s;"""
                    cursor.execute(query, VALUES)
                    show.set_country_list(cursor.fetchall())

                    query = """SELECT li.listed_in FROM projeto_database_db.show_tbl AS s INNER JOIN projeto_database_db.show_listed_in_tbl AS sli ON sli.id_show = s.id INNER JOIN projeto_database_db.listed_in_tbl AS li ON li.id = sli.id_listed_in WHERE s.id = %s;"""
                    cursor.execute(query, VALUES)
                    show.set_listed_in_list(cursor.fetchall())

                    query = """SELECT c.cast FROM projeto_database_db.show_tbl AS s INNER JOIN projeto_database_db.show_cast_tbl AS sc ON sc.id_show = s.id INNER JOIN projeto_database_db.cast_tbl AS c ON c.id = sc.id_cast WHERE s.id = %s;"""
                    cursor.execute(query, VALUES)
                    show.set_country_list(cursor.fetchall())

                    return show

                return None

    except mysql.connector.Error as msce:
        raise RuntimeError("Erro ao buscar o ID:", msce)


def insert_into_show_tbl_by_csv(csv_path: str) -> None:
    data = read_csv_to_dict(csv_path, EXCEPT_FILL_DB_BY_CSV)

    with conect_to_db() as conn:
        with conn.cursor() as cursor:
            for row in data.values():
                INSERT_QUERY = "INSERT INTO `show_tbl` (title, date_added, release_year, duration, description, type_id, rating_id) VALUES (%s, %s, %s, %s, %s, %s, %s);"

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


def insert_into_join_table(conn, column, value, join_tbl, id_source_tbl, show_id):
    with conn.cursor() as cursor:
        try:
            SOURCE_TABLE = f"{column}_tbl"
            select_query = f"SELECT id FROM `{SOURCE_TABLE}` WHERE `{column}` = %s;"
            SOURCE_ID = find_id(select_query, value)

            if not SOURCE_ID:
                return

            INSERT_QUERY = (
                f"INSERT INTO `{join_tbl}` (id_show, {id_source_tbl}) VALUES (%s, %s);"
            )

            cursor.execute(INSERT_QUERY, (show_id, SOURCE_ID))

            print(f'Dado inserido com sucesso na tabela "{join_tbl}"!\n')

        except mysql.connector.Error as msce:
            raise RuntimeError("Erro ao buscar o ID:", msce)


def insert_into_N_N_tbl_by_csv(csv_path: str) -> None:
    data = read_csv_to_dict(csv_path, EXCEPT_FILL_DB_BY_CSV)

    with conect_to_db() as conn:
        for row in data.values():
            select_query = "SELECT id FROM `show_tbl` WHERE `title` = %s;"
            SHOW_ID = find_id(select_query, row["title"])

            for column in row:
                if column not in SOURECES_TABLES:
                    continue

                JOIN_TBL = f"show_{column}_tbl"
                ID_SOURCE_TBL = f"id_{column}"
                values = [row[column]]

                if values[0] and ("," in values[0]):
                    values[0] = tuple(value.strip() for value in values[0].split(","))

                if values[0]:
                    # Case "not None" value in values[0]":
                    for value in values:
                        if isinstance(value, tuple):
                            # In case of a multivalored value:
                            values = value
                            for value in values:
                                insert_into_join_table(
                                    conn,
                                    column,
                                    value,
                                    JOIN_TBL,
                                    ID_SOURCE_TBL,
                                    SHOW_ID,
                                )
                        else:
                            # In case of a unique value:
                            insert_into_join_table(
                                conn,
                                column,
                                value,
                                JOIN_TBL,
                                ID_SOURCE_TBL,
                                SHOW_ID,
                            )
        conn.commit()
