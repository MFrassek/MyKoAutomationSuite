import re
from helper import connect_to_db, disconnect_from_db


def add_new_volunteer_and_position(db_name):
    conn, c = connect_to_db(db_name)
    volunteerName = input("Name:\n")
    add_entry_to_table_volunteers(c, volunteerName)
    for position_name in prompt_position_names():
        add_entry_to_table_x(c, position_name, volunteerName)
    disconnect_from_db(conn)


def add_entry_to_table_volunteers(c, volunteerName):
    gender, birthDate = prompt_gender_and_birthDate()
    c.execute(
        "INSERT INTO volunteers VALUES ('{}', '{}', '{}')"
        .format(volunteerName, gender, birthDate))


def prompt_gender_and_birthDate():
    gender = ""
    while gender not in ["f", "m", "d"]:
        gender = input("Gender [f, m or d]:\n")
    birthDate = ""
    while not re.match(r"\d\d\d\d-\d\d-\d\d", birthDate):
        birthDate = input("Birthdate [YYYY-MM-DD]:\n")
    return gender, birthDate


def prompt_position_names():
    return [position.strip() for position in
            input("Comma separated positions [mysecs, myvers]:\n").split(",")]


def add_entry_to_table_x(c, table, volunteerName):
    regionName, startDate = prompt_regionName_and_startDate()
    c.execute(
        "INSERT INTO {} VALUES ('{}', '{}', '{}', '');"
        .format(table, volunteerName, regionName, startDate))


def prompt_regionName_and_startDate():
    regionName = input("Region name:\n")
    startDate = ""
    while not re.match(r"\d\d\d\d-\d\d-\d\d", startDate):
        startDate = input("Start date [YYYY-MM-DD]:\n")
    return regionName, startDate


if __name__ == '__main__':
    add_new_volunteer_and_position("MY-Ko.db")
