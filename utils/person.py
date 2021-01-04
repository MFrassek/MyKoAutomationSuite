class Person:
    def __init__(self, name: str, birth_date: str, gender: str, region: str):
        self._name = name
        self._birth_date = birth_date
        self._gender = gender
        self._region = region

    def __str__(self):
        return f"{self._name}, born: {self._birth_date}, " \
            + f"gender: {self._gender}, region: {self._region}"

    @property
    def name(self):
        return self._name

    @property
    def birth_date(self):
        return self._birth_date

    @property
    def gender(self):
        return self._gender

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, region):
        assert isinstance(region, str), \
            "'region' can only be set to type string."
        self._region = region


class Volunteer(Person):
    def __init__(
            self, name: str, birth_date: str, gender: str,
            region: str, positions: list):
        super(Volunteer, self).__init__(
            name, birth_date, gender, region)
        self._positions = positions
