from helper import string_follows_input_pattern
from person import Volunteer
from position import Position


def add_new_volunteer_and_positions():
    volunteer_name = prompt_volunteer_name()
    add_new_volunteer(volunteer_name)
    for position_name in prompt_position_names():
        add_new_position(position_name, volunteer_name)


def add_new_volunteer(volunteer_name):
    new_volunteer = Volunteer(
        name=volunteer_name, birth_date=prompt_birth_date(),
        gender=prompt_gender())
    new_volunteer.add_to_db()


def add_new_position(title, volunteer_name):
    new_postion = Position(
        title=title, region=prompt_region_name(), held_by=volunteer_name,
        start_date=prompt_start_date(), end_date=prompt_end_date(),
        position_id=prompt_position_id())
    new_postion.add_to_db()


def prompt_volunteer_name():
    while True:
        volunteer_name = input("Name [a-üA-Ü ,-]:\n")
        if string_follows_input_pattern(volunteer_name, "name"):
            return volunteer_name


def prompt_gender():
    while True:
        gender = input("Gender [f, m, d, u]:\n")
        if string_follows_input_pattern(gender, "gender"):
            return gender


def prompt_birth_date():
    while True:
        birth_date = input("Birthdate [YYYY-MM-DD]:\n")
        if string_follows_input_pattern(birth_date, "date"):
            return birth_date


def prompt_position_names():
    return [position.strip() for position in
            input("Comma separated positions [MYSec, MY-VeranstalterIn]:\n")
            .split(",")]


def prompt_region_name():
    while True:
        region_name = input("Region name:\n")
        if string_follows_input_pattern(region_name, "name"):
            return region_name


def prompt_start_date():
    while True:
        start_date = input("Start date [YYYY-MM-DD]:\n")
        if string_follows_input_pattern(start_date, "date"):
            return start_date


def prompt_end_date():
    while True:
        end_date = input("End date [YYYY-MM-DD]:\n")
        if string_follows_input_pattern(end_date, "date"):
            return end_date


def prompt_position_id():
    while True:
        position_id = input("Position id:\n")
        if string_follows_input_pattern(position_id, "id"):
            return position_id


if __name__ == '__main__':
    add_new_volunteer_and_positions()
