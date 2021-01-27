from userInteraction import UserInteraction
from databaseConnection import DatabaseConnection
from person import Volunteer
from position import Position


def add_new_volunteer_and_positions():
    volunteer_name = UserInteraction.get_volunteer_name()
    add_new_volunteer(volunteer_name)
    for position_name in UserInteraction.get_position_names():
        add_new_position(position_name, volunteer_name)


def add_new_volunteer(volunteer_name):
    new_volunteer = Volunteer(
        name=volunteer_name, birth_date=UserInteraction.get_birth_date(),
        gender=UserInteraction.get_gender())
    new_volunteer.add_to_db()


def add_new_position(title, volunteer_name):
    new_postion = Position(
        title=title, region=UserInteraction.get_region_name(),
        held_by=volunteer_name, start_date=UserInteraction.get_start_date(),
        end_date=UserInteraction.get_end_date(),
        position_id=UserInteraction.get_position_id())
    new_postion.add_to_db()


if __name__ == '__main__':
    add_new_volunteer_and_positions()
    DatabaseConnection.close()
