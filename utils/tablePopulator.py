import abc


class TablePopulator(abc.ABC):
    data_path = "./data"

    @abc.abstractmethod
    def populate_table():
        pass

    @abc.abstractmethod
    def get_data_from_file():
        pass
