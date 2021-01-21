from tablePopulator import TablePopulator
from person import Volunteer


class VolunteerPopulator(TablePopulator):
    @classmethod
    def populate_table(cls):
        volunteer_data = cls.get_data_from_file()
        for volunteer in volunteer_data:
            Volunteer(
                name=volunteer[0], gender=volunteer[1],
                birth_date=volunteer[2]).add_to_db()

    @classmethod
    def get_data_from_file(cls):
        with open(f"{cls.data_path}/Volunteers.txt", "r") as volunteer_file:
            result = [line[:-1].split("\t") for line
                      in volunteer_file.readlines()]
        return result
