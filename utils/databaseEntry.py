import abc
from databaseConnection import DatabaseConnection
from sqlite3 import IntegrityError
import sys


class DatabaseEntry(abc.ABC):
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
    def get_details_fitting_data(cls, commands: list, **kwargs):
        assert len(commands) > 0, \
            "At least one specifying command must be given"
        db_conn = DatabaseConnection()
        return db_conn.query(
            f"""SELECT *
            FROM {cls.get_table_name(**kwargs)}
            WHERE """
            + " AND ".join(
             [cls.argument_name_to_column_name(command[0])
              + f" {command[1]} '{' '.join(command[2:])}'"
              for command in commands]))

    @classmethod
    def get_table_name(cls, **kwargs):
        return cls.table_name

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
        db_conn = DatabaseConnection()
        try:
            db_conn.change(self.get_insertion_command())
        except IntegrityError:
            print(f"{sys.exc_info()[0].__name__}: {sys.exc_info()[1]}")

    def update_in_db(self):
        db_conn = DatabaseConnection()
        db_conn.change(self.get_update_command())

    @abc.abstractmethod
    def get_insertion_command():
        pass

    def get_update_command():
        raise NotImplementedError

    def convert_YYYYMMDD_to_DDMMYYYY_date(self, date):
        return ".".join(date.split("-")[::-1])
