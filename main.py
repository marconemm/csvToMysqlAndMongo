from utils.funcoes import trata_data_frame, salva_valores_unicos
from utils.my_sql import insert_uniques_into_db
from utils import EXCECAO_VALORES_UNICOS, EXCECAO_INICIAIS_MAIUSCULAS

df = trata_data_frame("database/teste_data.csv", EXCECAO_INICIAIS_MAIUSCULAS)
# df = trata_data_frame("database/netflix_titles.csv")
PATHS_TUPLE = (
    "normalizado/type.csv",
    "normalizado/rating.csv",
    "normalizado/director.csv",
    "colocar_na_1FN/cast.csv",
    "colocar_na_1FN/country.csv",
    "colocar_na_1FN/listed_in.csv",
    "normalizado/show.csv",
)

COLUNAS_DICT = salva_valores_unicos(df, excecao=EXCECAO_VALORES_UNICOS)

insert_uniques_into_db(PATHS_TUPLE, COLUNAS_DICT)
