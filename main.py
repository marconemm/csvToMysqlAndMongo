from utils.funcoes import trata_data_frame, salva_valores_unicos
from utils.my_sql import insert_uniques_into_db, insert_into_show_tbl
from utils import EXCEPT_UNIQUE_VALUES, EXCEPT_CAPITAL_INITIALS

CSV_PATH = "database/teste_data.csv"
# CSV_PATH = "database/netflix_titles.csv"
PATHS_TUPLE = (
    "normalizado/type.csv",
    "normalizado/rating.csv",
    "normalizado/director.csv",
    "colocar_na_1FN/cast.csv",
    "colocar_na_1FN/country.csv",
    "colocar_na_1FN/listed_in.csv",
)

df = trata_data_frame(CSV_PATH, EXCEPT_CAPITAL_INITIALS)
COLUNAS_DICT = salva_valores_unicos(df, excecao=EXCEPT_UNIQUE_VALUES)

insert_uniques_into_db(PATHS_TUPLE, COLUNAS_DICT)
insert_into_show_tbl(CSV_PATH)
