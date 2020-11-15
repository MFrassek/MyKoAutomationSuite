from helper import connect_to_db, disconnect_from_db,\
    get_general_volunteer_details, get_position_details, \
    get_data_type_from_column_name, string_follows_input_pattern


def update_details(db_name):
    conn, c = connect_to_db(db_name)
    volunteerName = input("Name:\n")
    all_positions = get_all_positions(c, volunteerName)
    if all_positions:
        update_volunteer_details(c, volunteerName)
        for position in all_positions:
            print(position)
            update_position_details(c, volunteerName, position)
    else:
        print("No positions found for this name")
    disconnect_from_db(conn)


def get_all_positions(c, volunteerName):
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_positions = []
    for table in c.fetchall():
        c.execute("PRAGMA table_info({})".format(table[0]))
        if c.fetchall()[0][1] == "volunteerName" and table[0] != "volunteers":
            c.execute("SELECT * FROM {} WHERE volunteerName = '{}';"
                      .format(table[0], volunteerName))
            if len(c.fetchall()) >= 1:
                all_positions.append(table[0])
    return all_positions


def update_volunteer_details(c, volunteerName):
    _, gender, birthDate = get_general_volunteer_details(c, volunteerName)
    update_value_in_table(c, volunteerName, "volunteers", "gender", gender)
    update_value_in_table(
        c, volunteerName, "volunteers", "birthDate", birthDate)


def update_position_details(c, volunteerName, position):
    _, regionName, startDate, endDate = get_position_details(
        c, volunteerName, position)
    update_value_in_table(c, volunteerName, position, "regionName", regionName)
    update_value_in_table(c, volunteerName, position, "startDate", startDate)
    update_value_in_table(c, volunteerName, position, "endDate", endDate)


def update_value_in_table(c, volunteerName, table, column_name, value):
    data_type = get_data_type_from_column_name(column_name)
    while True:
        new_value = input(
            f"Current {column_name}: {value}\nNew {column_name}: ")
        if string_follows_input_pattern(new_value, data_type):
            break
    if new_value:
        c.execute(f"""UPDATE {table}
            SET {column_name} = '{new_value}'
            WHERE volunteerName = '{volunteerName}';""")


if __name__ == '__main__':
    update_details("MY-Ko.db")
