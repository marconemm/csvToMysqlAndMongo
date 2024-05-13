UTF8 = "utf_8"
#CSV_PATH = "database/teste_data2.csv"
CSV_PATH = "database/netflix_titles.csv"
EXCEPT_FILL_DB_BY_CSV = ("release_year", "date_added", "duration")
EXCEPT_UNIQUE_VALUES = ("date_added", "description")
EXCEPT_CAPITAL_INITIALS = ("rating", "duration", "description")
SHOW_TBL_COLUMNS = (
    "title",
    "date_added",
    "release_year",
    "duration",
    "description",
    "type",
    "rating_id",
)
SOURECES_TABLES = ("director", "cast", "country", "listed_in")
