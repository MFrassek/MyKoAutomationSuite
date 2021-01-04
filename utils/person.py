from position import Position
from helper import connect_to_db, disconnect_from_db


class Person:
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


class Volunteer(Person):
    def __init__(
            self, name: str, birth_date: str, gender: str):
        super(Volunteer, self).__init__(
            name, birth_date, gender)
        self._positions = self.get_held_positions()

    def __repr__(self):
        return "Volunteer " + super().__repr__() + "\n\t" \
            + ("\n\t").join(list(map(str, self._positions)))

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

    @staticmethod
    def create_all_volunteers_fitting_data(**kwargs):
        conn, c = connect_to_db(Position.db_name)
        volunteers = [
            Volunteer.create_volunteer_from_db_data_tuple(data_tuple)
            for data_tuple
            in Volunteer.get_volunteer_details_fitting_data(c, **kwargs)]
        disconnect_from_db(conn)
        return volunteers

    @staticmethod
    def create_volunteer_from_db_data_tuple(data_tuple: tuple):
        name, birth_date, gender = data_tuple
        return Volunteer(name, birth_date, gender)

    @staticmethod
    def get_volunteer_details_fitting_data(c, **kwargs):
        assert len(kwargs) > 0, \
            "At least one specifying key word argument must be given"
        c.execute(
            """SELECT *
            FROM volunteers
            WHERE """
            + " AND ".join(
             [Volunteer.kwarg_to_column_name(kwarg) + f" = '{kwargs[kwarg]}'"
              for kwarg in kwargs.keys()]))
        return c.fetchall()

    @staticmethod
    def kwarg_to_column_name(kwarg: str):
        kwarg_to_column_name = {
            "name": "volunteerName",
            "birth_date": "birthDate",
            "gender": "gender"}
        return kwarg_to_column_name[kwarg]
