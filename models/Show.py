import datetime

class Show:

    def __init__(self) -> None:
        self.id = self.release_year = 0
        self.type = self.title = self.rating = self.duration = self.description = ""
        self.director_list = self.cast_calist = self.country_list = []
        self.listed_in_list = []
        self.date_added = datetime.date.today()

    def __str__(self) -> str:
        return f"Eu sou um objeto Show, e fui criado no dia: {self.date_added}"