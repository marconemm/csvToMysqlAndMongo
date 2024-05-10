from utils.funcoes import trata_data_frame, salva_valores_unicos
from utils.my_sql import executar_script_sql

df = trata_data_frame("database/teste_data.csv")
#df = trata_data_frame("database/netflix_titles.csv")
COLUNAS_DICT = {}

# Obém todos valores únicos de cada coluna:
salva_valores_unicos(df, save_in=COLUNAS_DICT, excecao=("date_added", "description"))

# Insere os dados punicos em todas as tabelas in de coluna única:
executar_script_sql("database/normalizado/type.csv", COLUNAS_DICT)
executar_script_sql("database/normalizado/rating.csv", COLUNAS_DICT)
executar_script_sql("database/normalizado/director.csv", COLUNAS_DICT)
executar_script_sql("database/colocar_na_1FN/cast.csv", COLUNAS_DICT)
executar_script_sql("database/colocar_na_1FN/country.csv", COLUNAS_DICT)
executar_script_sql("database/colocar_na_1FN/listed_in.csv", COLUNAS_DICT)
# executar_script_sql("database/normalizado/show.csv", COLUNAS_DICT)
