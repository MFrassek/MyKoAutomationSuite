from position import Position


class Person:
    def __init__(self, name: str, birth_date: str, gender: str, region: str):
        self._name = name
        self._birth_date = birth_date
        self._gender = gender
        self._region = region

    def __repr__(self):
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
            region: str):
        super(Volunteer, self).__init__(
            name, birth_date, gender, region)
        self._positions = self.get_held_positions()

    def __repr__(self):
        return "Volunteer " + super().__repr__()

    @property
    def positions(self):
        return self._positions

    def get_held_positions(self):
        all_titles_in_use = ["MYSec"]
        positions = []
        for title in all_titles_in_use:
            positions.extend(Position.create_all_positions_fitting_data(
                title, held_by=self._name))
        return tuple(positions)
