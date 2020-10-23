import sqlite3


def add_new_volunteer_and_position(db_name):
    conn, c = connect_to_db(db_name)
    volunteerName = input("Name:\n")
    add_entry_to_table_volunteers(c, volunteerName)
    for position_name in prompt_position_names():
        add_entry_to_table_x(c, position_name, volunteerName)
    deconnect_from_db(conn)


def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn, conn.cursor()


def add_entry_to_table_volunteers(c, volunteerName):
    gender, birthDate = prompt_gender_and_birthDate()
    c.execute(
        "INSERT INTO volunteers VALUES ('{}', '{}', '{}')"
        .format(volunteerName, gender, birthDate))


def prompt_gender_and_birthDate():
    gender = input("Gender [f, m or d]:\n")
    birthDate = input("Birthdate [YYYY-MM-DD]:\n")
    return gender, birthDate


def prompt_position_names():
    return input("Comma separated positions [mysecs, myvers]:\n").split(",")


def add_entry_to_table_x(c, table, volunteerName):
    regionName, startDate = prompt_regionName_and_startDate()
    c.execute(
        "INSERT INTO {} VALUES ('{}', '{}', '{}', '');"
        .format(table, volunteerName, regionName, startDate))


def prompt_regionName_and_startDate():
    regionName = input("Region name:\n")
    startDate = input("Start date [YYYY-MM-DD]:\n")
    return regionName, startDate


def deconnect_from_db(conn):
    conn.commit()
    conn.close()


if __name__ == '__main__':
    add_new_volunteer_and_position("MY-Ko.db")
