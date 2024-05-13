import datetime


class Show:

    def __init__(self) -> None:
        self.id = self.release_year = 0
        self.type = self.title = self.rating = self.duration = self.description = ""
        self.director_list = []
        self.cast_list = []
        self.country_list = []
        self.listed_in_list = []
        self.date_added = datetime.date.today()

    def __str__(self):
        properties = (
            f"ID: {self.id}",
            f"Release Year: {self.release_year}",
            f"Type: {self.type}",
            f"Title: {self.title}",
            f"Rating: {self.rating}",
            f"Duration: {self.duration}",
            f"Description: {self.description}",
            f"Directors: {', '.join(self.director_list)}",
            f"Cast: {', '.join(self.cast_list)}",
            f"Countries: {', '.join(self.country_list)}",
            f"Listed In: {', '.join(self.listed_in_list)}",
            f"Date Added: {self.date_added}",
        )

        return (
            "\n"
            + self.__class__.__name__
            + " <"
            + str(id(self))
            + ">:\n{"
            + ", ".join(properties)
            + " }\n"
        )

    def set_show_attr(self, properties_dict_list: list[dict]) -> None:
        for row in properties_dict_list:
            for key, value in row.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    def set_director_list(self, properties_dict_list: list | dict) -> None:
        self._set_self_list(self.director_list, properties_dict_list)

    def set_country_list(self, properties_dict_list: list | dict) -> None:
        self._set_self_list(self.country_list, properties_dict_list)

    def set_listed_in_list(self, properties_dict_list: list | dict) -> None:
        self._set_self_list(self.listed_in_list, properties_dict_list)

    def set_cast_list(self, properties_dict_list: list | dict) -> None:
        self._set_self_list(self.cast_list, properties_dict_list)

    def _set_self_list(self, self_list: list, properties_dict_list: list | dict):
        if isinstance(properties_dict_list, list):
            for row in properties_dict_list:
                for value in row.values():
                    self_list.append(value)

        else:
            for value in properties_dict_list.values():
                self_list.append(value)
