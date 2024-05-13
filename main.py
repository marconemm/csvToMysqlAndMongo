from utils.my_sql import mysql_select_show_by_id
from utils.mongo_db import mongo_insert_show_into_db_by_id

def find_in_mysql_and_insert_into_mongo_by_id(id:int) -> None:
    mysql_select_show_by_id(id)
    mongo_insert_show_into_db_by_id(id)
    

find_in_mysql_and_insert_into_mongo_by_id(2)