import abc
from rawDataAccessMixin import RawDataAccessMixin


class TablePopulator(abc.ABC, RawDataAccessMixin):
    @abc.abstractmethod
    def populate_table():
        pass

    @abc.abstractmethod
    def get_data_from_file():
        pass
