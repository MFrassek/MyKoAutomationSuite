from tablePopulator import TablePopulator
from position import Position


class PositionPopulator(TablePopulator):
    @classmethod
    def populate_table(cls):
        position_data = cls.get_data_from_file()
        for position in position_data:
            Position(
                title=position[0], region=position[2], held_by=position[1],
                start_date=position[3], end_date=position[4]).add_to_db()

    @classmethod
    def get_data_from_file(cls):
        with open(f"{cls.data_path}/Positions.txt", "r") as data_file:
            result = [line[:-1].split("\t") for line in data_file.readlines()]
        return result
