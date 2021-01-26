from tablePopulator import TablePopulator
from weekendParticipation import WeekendParticipation
import os
import csv


class WeekendParticipationPopulator(TablePopulator):
    @classmethod
    def populate_table(cls):
        weekend_participation_data = cls.get_data_from_file()
        for weekend_participation in weekend_participation_data:
            WeekendParticipation(
                weekend_id=weekend_participation[0],
                participant_name=weekend_participation[1]).add_to_db()

    @classmethod
    def get_data_from_file(cls):
        result = []
        for weekend_file_name in os.listdir(f"{cls.data_path}/participants"):
            weekend_id = weekend_file_name.split("_")[0]
            with open(f"{cls.data_path}/participants/{weekend_file_name}",
                      encoding='latin1') as participants_file:
                participants = csv.reader(participants_file)
                next(participants)
                result.extend([[weekend_id, x[8]] for x in participants])
        return result
