import re
from helper import connect_to_db, disconnect_from_db
from sqlite3 import IntegrityError
import sys


class Position():
    db_name = "MY-Ko.db"

    def __init__(
            self, title: str, region: str, held_by: str,
            start_date: str, end_date: str = "", position_id: str = None):
        self._title = title
        self._held_by = held_by
        self._region = region
        self._start_date = start_date
        self._end_date = end_date
        self._position_id = position_id

    def __str__(self):
        if self._end_date:
            return f"{self._title} {self._region}: Held by {self._held_by}" \
                + f" from {self._start_date} until {self._end_date}"
        else:
            return f"{self._title} {self._region}: Held by {self._held_by}" \
                + f" since {self._start_date}"

    @property
    def title(self):
        return self._title

    @property
    def position_id(self):
        return self._position_id

    @property
    def held_by(self):
        return self._held_by

    @property
    def region(self):
        return self._region

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, end_date: str):
        assert isinstance(end_date, str), \
            "'end_date' can only be set to type string."
        assert re.match("\d{4}-\d{2}-\d{2}", end_date), \
            "'end_date' does not match data format YYYY-MM-DD"
        self._end_date = end_date

    @staticmethod
    def create_all_positions_fitting_data(title: str, **kwargs):
        conn, c = connect_to_db(Position.db_name)
        positions = [
            Position.create_position_from_db_data_tuple(title, data_tuple)
            for data_tuple
            in Position.get_position_details_fitting_data(c, title, **kwargs)]
        disconnect_from_db(conn)
        return positions

    @staticmethod
    def create_position_from_db_data_tuple(title: str, data_tuple: tuple):
        position_id, held_by, region, start_date, end_date = data_tuple
        return Position(
            title, region, held_by, start_date, end_date, position_id)

    @staticmethod
    def get_position_details_fitting_data(c, title: str, **kwargs):
        assert len(kwargs) > 0, \
            "At least one specifying key word argument must be given"
        c.execute(
            f"""SELECT *
            FROM {Position.title_to_table_name(title)}
            WHERE """
            + " AND ".join(
                [Position.kwarg_to_column_name(kwarg) + f" = '{kwargs[kwarg]}'"
                 for kwarg in kwargs.keys()]))
        return c.fetchall()

    @staticmethod
    def title_to_table_name(title: str):
        title_to_table_name = {
            "MYSec": "mysecs",
            "MY-VeranstalterIn": "myvers",
            "MY-Weekend Orga": "myweorgas"}
        return title_to_table_name[title]

    @staticmethod
    def kwarg_to_column_name(kwarg: str):
        kwarg_to_column_name = {
            "held_by": "volunteerName",
            "region": "regionName",
            "start_date": "startDate",
            "end_date": "endDate",
            "position_id": "positionId"}
        return kwarg_to_column_name[kwarg]

    def add_to_db(self):
        conn, c = connect_to_db(Position.db_name)
        try:
            if self._position_id:
                c.execute(self.get_command_for_db_insertion_with_id())
            else:
                c.execute(self.get_command_for_db_insertion_without_id())
        except IntegrityError:
            print(f"{sys.exc_info()[0].__name__}: {sys.exc_info()[1]}")
        disconnect_from_db(conn)

    def get_command_for_db_insertion_with_id(self):
        return f"""INSERT INTO {Position.title_to_table_name(self._title)}(
                positionId, volunteerName,
                regionName, startDate, endDate)
            VALUES (
                {self._position_id}, '{self._held_by}',
                '{self._region}', '{self._start_date}',
                '{self._end_date}');"""

    def get_command_for_db_insertion_without_id(self):
        return f"""INSERT INTO {Position.title_to_table_name(self._title)}(
                volunteerName,
                regionName, startDate, endDate)
            VALUES (
                '{self._held_by}',
                '{self._region}', '{self._start_date}',
                '{self._end_date}');"""

    def update_in_db(self):
        conn, c = connect_to_db(Position.db_name)
        c.execute(f"""UPDATE {Position.title_to_table_name(self._title)}
            SET endDate = '{self._end_date}'
            WHERE positionId = '{self._position_id}';""")
        disconnect_from_db(conn)
