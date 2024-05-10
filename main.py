from utils.funcoes import trata_data_frame, salva_valores_unicos, cria_sub_dicionario

df = trata_data_frame("database/teste_data.csv")
# df = trata_data_frame("database/netflix_titles.csv")
COLUNAS_DICT = {}

# Obém todos valores únicos de cada coluna:
salva_valores_unicos(df, save_in=COLUNAS_DICT, excecao=("date_added", "description"))

# Cria os sub dicionários, conforme arquivos CSV separados manualmente:
dict_show = cria_sub_dicionario("database/normalizado/show.csv", COLUNAS_DICT)
dict_type = cria_sub_dicionario("database/normalizado/type.csv", COLUNAS_DICT)
dict_diretor = cria_sub_dicionario("database/normalizado/diretor.csv", COLUNAS_DICT)
dict_rating = cria_sub_dicionario("database/normalizado/rating.csv", COLUNAS_DICT)
dict_cast = cria_sub_dicionario("database/colocar_na_1FN/cast.csv", COLUNAS_DICT)
dict_country = cria_sub_dicionario("database/colocar_na_1FN/country.csv", COLUNAS_DICT)
dict_listed_in = cria_sub_dicionario("database/colocar_na_1FN/listed_in.csv", COLUNAS_DICT)

