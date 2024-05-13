from pymongo.database import Database
from models.Show import Show


def conect_to_db() -> Database:
    """Conecta com o banco de dados e retorna uma instância do banco de dados, conforme configuração do ambiente.

    Returns:
        MongoClient: instancia do banco de dados do MongoDB.
    """
    import pymongo
    from dotenv import load_dotenv
    import os

    load_dotenv()

    client = pymongo.MongoClient(
        os.getenv("DATABASE_HOST"), int(os.getenv("MONGO_DB_PORT"))
    )
    
    return client[os.getenv("DATABASE_NAME")]



def mongo_insert_show_into_db_by_id(id: int) -> None:
    from utils.my_sql import mysql_select_show_by_id

    show = mysql_select_show_by_id(id)
    show.date_added = show.date_added.isoformat()
    show = show.__dict__
    DB = conect_to_db()
 
    result = DB.show.insert_one(show)

    if result.inserted_id:
        print(f"\nObjeto Show inserido com sucesso! Id: {result.inserted_id}")
    else:
        print("Falha ao inserir objeto Show.")
