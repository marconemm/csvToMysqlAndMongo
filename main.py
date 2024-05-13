from utils.mongo_db import mongo_insert_show_into_db_by_id
import sys

id = sys.argv[1]

mongo_insert_show_into_db_by_id(id)
    