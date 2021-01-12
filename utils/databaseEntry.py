import abc
from helper import connect_to_db, disconnect_from_db


class DatabaseEntry(abc.ABC):
    db_name = "MY-Ko.db"

    @classmethod
    def create_all_entries_fitting_data(cls, commands: list, **kwargs):
        conn, c = connect_to_db(DatabaseEntry.db_name)
        entries = [
            cls.create_entry_from_db_data_tuple(data_tuple, **kwargs)
            for data_tuple
            in cls.get_entry_details_fitting_data(c, commands, **kwargs)]
        disconnect_from_db(conn)
        return entries

    @abc.abstractmethod
    def create_entry_from_db_data_tuple():
        pass

    @abc.abstractmethod
    def get_entry_details_fitting_data():
        pass

    @staticmethod
    def argument_name_to_column_name(argument_name: str):
        argument_name_to_column_name = {
            "name": "volunteerName",
            "birth_date": "birthDate",
            "gender": "gender",
            "held_by": "volunteerName",
            "region": "regionName",
            "start_date": "startDate",
            "end_date": "endDate",
            "position_id": "positionId"}
        return argument_name_to_column_name[argument_name]

    @staticmethod
    def title_to_table_name(title: str):
        title_to_table_name = {
            "MYSec": "mysecs",
            "MY-VeranstalterIn": "myvers",
            "MY-Weekend Orga": "myweorgas"}
        return title_to_table_name[title]
