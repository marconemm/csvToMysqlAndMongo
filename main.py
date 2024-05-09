import pandas as pd
from utils.funcoes import trata_data_frame, salva_valores_unicos, cria_sub_dict

df = trata_data_frame("database/teste_data.csv")
colunas_dict = {}

# Obém todos valores únicos de cada coluna:
salva_valores_unicos(df, save_in=colunas_dict, excecao=["date_added", "description"])

# Cria os sub dicionários, conforme arquivos CSV separados manualmente:
dict_show = cria_sub_dict("database/normalizado/show.csv", colunas_dict)
dict_type = cria_sub_dict("database/normalizado/type.csv", colunas_dict)
dict_diretor = cria_sub_dict("database/normalizado/diretor.csv", colunas_dict)
dict_rating = cria_sub_dict("database/normalizado/rating.csv", colunas_dict)
dict_cast = cria_sub_dict("database/colocar_na_1FN/cast.csv", colunas_dict)
dict_country = cria_sub_dict("database/colocar_na_1FN/country.csv", colunas_dict)
dict_listed_in = cria_sub_dict("database/colocar_na_1FN/listed_in.csv", colunas_dict)

