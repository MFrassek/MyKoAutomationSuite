from databaseEntry import DatabaseEntry
import re
from helper import connect_to_db, disconnect_from_db


class Position(DatabaseEntry):
    all_titles_in_use = ["MYSec"]

    def __init__(
            self, title: str, region: str, held_by: str,
            start_date: str, end_date: str = "", position_id: str = None):
        self._title = title
        self._held_by = held_by
        self._region = region
        self._start_date = start_date
        self._end_date = end_date
        self._position_id = position_id

    def __repr__(self):
        if self._end_date:
            return f"{self._title} {self._region}: Held by {self._held_by}" \
                + f" from {self._start_date} until {self._end_date}"
        else:
            return f"{self._title} {self._region}: Held by {self._held_by}" \
                + f" since {self._start_date}"

    def __hash__(self):
        return hash(self._title) ^ hash(self._held_by) ^ hash(self._region) \
            ^ hash(self._start_date) ^ hash(self._end_date)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.title == other.title \
                and self.held_by == other.held_by \
                and self.region == other.region \
                and self.start_date == other.start_date \
                and self.end_date == other.end_date
        else:
            return False

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
        assert end_date == "" or re.match("\\d{4}-\\d{2}-\\d{2}", end_date), \
            "'end_date' does not match data format YYYY-MM-DD"
        self._end_date = end_date

    @property
    def start_date_ddmmyyyy(self):
        return self.convert_YYYYMMDD_to_DDMMYYYY_date(self._start_date)

    @property
    def end_date_ddmmyyyy(self):
        return self.convert_YYYYMMDD_to_DDMMYYYY_date(self._end_date)

    @classmethod
    def create_from_db_data_tuple(cls, data_tuple: tuple, title: str):
        position_id, held_by, region, start_date, end_date = data_tuple
        return cls(
            title, region, held_by, start_date, end_date, position_id)

    @classmethod
    def get_table_name(cls, title):
        return cls.title_to_table_name(title)

    @classmethod
    def create_all_held_positions(cls, held_by: str):
        positions = []
        for title in cls.all_titles_in_use:
            positions.extend(cls.create_all_fitting_data(
                [["held_by", "=", held_by]], title=title))
        return positions

    def get_insertion_command(self):
        if self._position_id:
            return f"""INSERT INTO {
                self.__class__.title_to_table_name(self._title)}(
                    positionId, personName,
                    regionName, startDate, endDate)
                VALUES (
                    {self._position_id}, '{self._held_by}',
                    '{self._region}', '{self._start_date}',
                    '{self._end_date}');"""
        else:
            return f"""INSERT INTO {
                self.__class__.title_to_table_name(self._title)}(
                    personName,
                    regionName, startDate, endDate)
                VALUES (
                    '{self._held_by}', '{self._region}', '{self._start_date}',
                    '{self._end_date}');"""

    def update_in_db(self):
        conn, c = connect_to_db(self.__class__.db_name)
        c.execute(f"""UPDATE {self.__class__.title_to_table_name(self._title)}
            SET endDate = '{self._end_date}'
            WHERE positionId = '{self._position_id}';""")
        disconnect_from_db(conn)
