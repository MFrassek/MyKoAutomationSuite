from helper import get_relative_path_to_script
from person import Volunteer


class VolunteerPopulator():
    data_path = get_relative_path_to_script() + "/data"

    @classmethod
    def populate_table(cls):
        volunteer_data = cls.get_volunteer_data_from_file()
        for volunteer in volunteer_data:
            vol = Volunteer(
                *volunteer)
            vol.add_to_db()

    @classmethod
    def get_volunteer_data_from_file(cls):
        with open(f"{cls.data_path}/Volunteers.txt", "r") as volunteer_file:
            result = [line[:-1].split("\t") for line
                      in volunteer_file.readlines()]
        return result
