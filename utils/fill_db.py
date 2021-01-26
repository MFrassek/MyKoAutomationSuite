from helper import connect_to_db, disconnect_from_db, \
    get_relative_path_to_script
import csv
from regionPopulator import RegionPopulator
from volunteerPopulator import VolunteerPopulator
from positionPopulator import PositionPopulator
from weekendPopulator import WeekendPopulator
from participantPopulator import ParticipantPopulator
from weekendParticipationPopulator import WeekendParticipationPopulator

def fill_db(data_path, db_name):
    conn, c = connect_to_db(db_name)
    populate_all_tables(data_path, c)
    disconnect_from_db(conn)
    RegionPopulator.populate_table()
    VolunteerPopulator.populate_table()
    PositionPopulator.populate_table()
    WeekendPopulator.populate_table()
    ParticipantPopulator.populate_table()
    WeekendParticipationPopulator.populate_table()


def populate_all_tables(data_path, c):
    pass


if __name__ == '__main__':
    data_path = "{}/data".format(get_relative_path_to_script())
    fill_db(data_path, "MY-Ko.db")
