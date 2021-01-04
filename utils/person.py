class Person:
    def __init__(self, name: str, birth_date: str, gender: str, region: str):
        self._name = name
        self._birth_date = birth_date
        self._gender = gender
        self._region = region

    def __str__(self):
        return f"{self._name}, born: {self._birth_date}, " \
            + f"gender: {self._gender}, region: {self._region}"
