from regionPopulator import RegionPopulator
from volunteerPopulator import VolunteerPopulator
from positionPopulator import PositionPopulator
from weekendPopulator import WeekendPopulator
from participantPopulator import ParticipantPopulator
from weekendParticipationPopulator import WeekendParticipationPopulator
from databaseConnection import DatabaseConnection


def fill_db():
    RegionPopulator.populate_table()
    VolunteerPopulator.populate_table()
    PositionPopulator.populate_table()
    WeekendPopulator.populate_table()
    ParticipantPopulator.populate_table()
    WeekendParticipationPopulator.populate_table()


if __name__ == '__main__':
    fill_db()
    DatabaseConnection.close()
