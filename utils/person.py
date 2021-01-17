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


class Volunteer(Person):
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

    @classmethod
    def create_from_db_data_tuple(cls, data_tuple: tuple):
        name, birth_date, gender = data_tuple
        return cls(name, birth_date, gender)

    @classmethod
    def get_details_fitting_data(cls, commands: list):
        assert len(commands) > 0, \
            "At least one specifying command must be given"
        conn, c = connect_to_db(cls.db_name)
        c.execute(
            """SELECT *
            FROM volunteers
            WHERE """
            + " AND ".join(
             [cls.argument_name_to_column_name(command[0])
              + f" {command[1]} '{' '.join(command[2:])}'"
              for command in commands]))
        result = c.fetchall()
        disconnect_from_db(conn)
        return result

    def get_insertion_command(self):
        return f"""INSERT INTO volunteers (
                volunteerName, gender, birthDate)
            VALUES (
                '{self._name}', '{self._gender}', '{self._birth_date}');"""


def get_pronoun_from_gender(gender):
    pronouns = {"m": "er", "f": "sie", "d": "em", "n": "em"}
    return pronouns[gender]
