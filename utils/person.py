from databaseEntry import DatabaseEntry
from position import Position
from helper import connect_to_db, disconnect_from_db


class Person(DatabaseEntry):
    def __init__(self, name: str, gender: str, birth_date: str):
        self._name = name
        self._gender = gender
        self._birth_date = birth_date

    def __repr__(self):
        return f"{self._name}, gender: {self._gender}, " \
            + f"born: {self._birth_date}"

    def __hash__(self):
        return hash(self._name) ^ hash(self._gender) ^ hash(self._birth_date)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name \
                and self.gender == other.gender \
                and self.birth_date == other.birth_date
        else:
            return False

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
    def pronoun(self):
        return get_pronoun_from_gender(self._gender)

    @property
    def first_name(self):
        return self._name.split(" ")[0]

    @property
    def base_name(self):
        return self._name.replace(" ", "_")

    @classmethod
    def create_from_db_data_tuple(cls, data_tuple: tuple):
        name, birth_date, gender = data_tuple
        return cls(name, birth_date, gender)

    def get_insertion_command(self):
        return f"""INSERT INTO {self.__class__.table_name} (
                personName, gender, birthDate)
            VALUES (
                '{self._name}', '{self._gender}', '{self._birth_date}');"""


class Volunteer(Person):
    table_name = "volunteers"

    def __init__(
            self, name: str, gender: str, birth_date: str):
        super(Volunteer, self).__init__(
            name=name, gender=gender, birth_date=birth_date)
        self._positions = tuple(Position.create_all_held_positions(self._name))

    def __repr__(self):
        return "Volunteer " + super().__repr__() + "\n\t" \
            + ("\n\t").join(list(map(str, self._positions)))

    @property
    def positions(self):
        return self._positions


class Participant(Person):
    table_name = "participants"

    def __init__(
            self, name: str, gender: str, birth_date: str):
        super(Participant, self).__init__(
            name=name, gender=gender, birth_date=birth_date)

    def __repr__(self):
        return "Participant " + super().__repr__()


def get_pronoun_from_gender(gender):
    pronouns = {"m": "er", "f": "sie", "d": "em", "n": "em"}
    return pronouns[gender]
