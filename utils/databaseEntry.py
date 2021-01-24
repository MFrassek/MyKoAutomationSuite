import abc
from helper import connect_to_db, disconnect_from_db
from sqlite3 import IntegrityError
import sys


class DatabaseEntry(abc.ABC):
    db_name = "MY-Ko.db"

    @classmethod
    def create_all_fitting_data(cls, commands: list, **kwargs):
        entries = [
            cls.create_from_db_data_tuple(data_tuple, **kwargs)
            for data_tuple
            in cls.get_details_fitting_data(commands, **kwargs)]
        return entries

    @abc.abstractmethod
    def create_from_db_data_tuple():
        pass

    @classmethod
    def get_details_fitting_data(cls, commands: list):
        assert len(commands) > 0, \
            "At least one specifying command must be given"
        conn, c = connect_to_db(cls.db_name)
        c.execute(
            f"""SELECT *
            FROM {cls.table_name}
            WHERE """
            + " AND ".join(
             [cls.argument_name_to_column_name(command[0])
              + f" {command[1]} '{' '.join(command[2:])}'"
              for command in commands]))
        result = c.fetchall()
        disconnect_from_db(conn)
        return result

    @classmethod
    def create_all(cls, **kwargs):
        return cls.create_all_fitting_data([["", "=", ""]], **kwargs)

    @staticmethod
    def argument_name_to_column_name(argument_name: str):
        argument_name_to_column_name = {
            "": "''",
            "name": "personName",
            "birth_date": "birthDate",
            "gender": "gender",
            "held_by": "personName",
            "region": "regionName",
            "start_date": "startDate",
            "end_date": "endDate",
            "position_id": "positionId",
            "region_id": "regionId",
            "m_count": "mCount",
            "my_count": "myCount",
            "weekend_id": "weekendId",
            "weekend_name": "weekendName",
            "weekend_location": "weekendLocation"}
        return argument_name_to_column_name[argument_name]

    @staticmethod
    def title_to_table_name(title: str):
        title_to_table_name = {
            "MYSec": "mysecs",
            "MY-VeranstalterIn": "myvers",
            "MY-Weekend Orga": "myweorgas"}
        return title_to_table_name[title]

    def add_to_db(self):
        conn, c = connect_to_db(self.__class__.db_name)
        try:
            c.execute(self.get_insertion_command())
        except IntegrityError:
            print(f"{sys.exc_info()[0].__name__}: {sys.exc_info()[1]}")
        disconnect_from_db(conn)

    @abc.abstractmethod
    def get_insertion_command():
        pass

    def convert_YYYYMMDD_to_DDMMYYYY_date(self, date):
        return ".".join(date.split("-")[::-1])
