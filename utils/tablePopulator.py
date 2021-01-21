from helper import get_relative_path_to_script
import abc


class TablePopulator(abc.ABC):
    data_path = get_relative_path_to_script() + "/data"

    @abc.abstractmethod
    def populate_table():
        pass

    @abc.abstractmethod
    def get_data_from_file():
        pass
