import re


class Position():
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

    @staticmethod
    def create_position_from_db_data_tuple(title: str, data_tuple: tuple):
        position_id, held_by, region, start_date, end_date = data_tuple
        return Position(
            title, region, held_by, start_date, end_date, position_id)

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