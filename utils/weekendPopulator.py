from tablePopulator import TablePopulator
from weekend import Weekend


class WeekendPopulator(TablePopulator):
    @classmethod
    def populate_table(cls):
        weekend_data = cls.get_data_from_file()
        for weekend in weekend_data:
            Weekend(
                id_=weekend[0], name=weekend[1], location=weekend[2],
                start_date=weekend[3], end_date=weekend[4],
                region_name=weekend[5]).add_to_db()

    @classmethod
    def get_data_from_file(cls):
        with open(f"{cls.data_path}/Weekends.txt", "r") as volunteer_file:
            result = [line[:-1].split("\t") for line
                      in volunteer_file.readlines()]
        return result
