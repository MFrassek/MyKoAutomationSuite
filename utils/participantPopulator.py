from tablePopulator import TablePopulator
from person import Participant
import os
import csv


class ParticipantPopulator(TablePopulator):
    @classmethod
    def populate_table(cls):
        participant_data = cls.get_data_from_file()
        for participant in participant_data:
            Participant(
                name=participant[8], gender=participant[9],
                birth_date=cls.convert_DDMMYYYY_to_YYYYMMDD_date(
                    participant[10])).add_to_db()

    @classmethod
    def get_data_from_file(cls):
        result = []
        for weekend_file_name in os.listdir(f"{cls.data_path}/participants"):
            with open(f"{cls.data_path}/participants/{weekend_file_name}",
                      encoding='latin1') as participants_file:
                participants = csv.reader(participants_file)
                next(participants)
                result.extend([x for x in participants])
        return result

    @classmethod
    def convert_DDMMYYYY_to_YYYYMMDD_date(cls, date):
        return "-".join(date.split(".")[::-1])
