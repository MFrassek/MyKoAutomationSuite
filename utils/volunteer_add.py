from helper import connect_to_db, disconnect_from_db, \
    string_follows_input_pattern


def add_new_volunteer_and_position(db_name):
    conn, c = connect_to_db(db_name)
    while True:
        volunteerName = input("Name [a-üA-Ü ,-]:\n")
        if string_follows_input_pattern(volunteerName, "name"):
            break
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
    while True:
        gender = input("Gender [f, m, d, u]:\n")
        if string_follows_input_pattern(gender, "gender"):
            break
    while True:
        birthDate = input("Birthdate [YYYY-MM-DD]:\n")
        if string_follows_input_pattern(birthDate, "date"):
            break
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
    while True:
        regionName = input("Region name:\n")
        if string_follows_input_pattern(regionName, "name"):
            break
    while True:
        startDate = input("Start date [YYYY-MM-DD]:\n")
        if string_follows_input_pattern(startDate, "date"):
            break
    return regionName, startDate


if __name__ == '__main__':
    add_new_volunteer_and_position("MY-Ko.db")
