from helper import connect_to_db, disconnect_from_db,\
    get_general_volunteer_details, get_position_details


def get_all_positions(c, volunteerName):
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_positions = []
    for table in c.fetchall():
        c.execute("PRAGMA table_info({})".format(table[0]))
        if c.fetchall()[0][1] == "volunteerName" and table[0] != "volunteers":
            c.execute("SELECT * FROM {} WHERE volunteerName = '{}';"
                      .format(table[0], volunteerName))
            if len(c.fetchall()) >= 1:
                print(table[0])
                all_positions.append(table[0])
    return all_positions
