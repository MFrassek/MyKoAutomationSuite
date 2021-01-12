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
