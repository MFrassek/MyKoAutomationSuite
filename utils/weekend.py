from databaseEntry import DatabaseEntry
from helper import connect_to_db, disconnect_from_db


class Weekend(DatabaseEntry):
    def __init__(
            self, id_: int, name: str, location: str, start_date: str,
            end_date: str, region_name: str):
        self._id = id_
        self._name = name
        self._location = location
        self._start_date = start_date
        self._end_date = end_date
        self._region_name = region_name

    def __repr__(self):
        return f"Weekend: {self._name} from {self._start_date}" \
            f" to {self._end_date}"

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._location

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def region_name(self):
        return self._region_name

    @classmethod
    def create_from_db_data_tuple(cls, data_tuple: tuple):
        return cls(*data_tuple)

    @classmethod
    def get_details_fitting_data(cls, commands: list):
        assert len(commands) > 0, \
            "At least one specifying command must be given"
        conn, c = connect_to_db(cls.db_name)
        c.execute(
            """SELECT *
            FROM weekends
            WHERE """
            + " AND ".join(
             [cls.argument_name_to_column_name(command[0])
              + f" {command[1]} '{' '.join(command[2:])}'"
              for command in commands]))
        result = c.fetchall()
        disconnect_from_db(conn)
        return result

    @classmethod
    def create_by_name(cls, name: str):
        return cls.create_all_fitting_data([["weekend_name", "=", name]])[0]

    @classmethod
    def create_by_id(cls, id_: int):
        return cls.create_all_fitting_data([["weekend_id", "=", str(id_)]])[0]

    def get_insertion_command(self):
        return f"""INSERT INTO weekends (
                weekendId, weekendName, weekendLocation,
                startDate, endDate, regionName)
            VALUES (
                '{self._id}', '{self._name}', '{self._location}',
                '{self._start_date}', '{self._end_date}',
                '{self._region_name}');"""
