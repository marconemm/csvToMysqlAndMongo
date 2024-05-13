import time
from utils.funcoes import trata_data_frame, salva_valores_unicos
from utils.my_sql import (
    insert_into_sources_tbl_by_csv,
    insert_into_show_tbl_by_csv,
    insert_into_N_N_tbl_by_csv,
)
from utils import CSV_PATH, EXCEPT_UNIQUE_VALUES, EXCEPT_CAPITAL_INITIALS

inicio = time.time()
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

insert_into_sources_tbl_by_csv(PATHS_TUPLE, COLUNAS_DICT)
insert_into_show_tbl_by_csv(CSV_PATH)
insert_into_N_N_tbl_by_csv(CSV_PATH)

fim = time.time()

print("\n\n--\nTodos os dados foram inseridos no banco de dados!")
print("Tempo de execução:", fim - inicio, "segundos")
