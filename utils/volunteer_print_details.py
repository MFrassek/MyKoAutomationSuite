from helper import connect_to_db, deconnect_from_db


def print_all_volunteer_details(db_name):
    conn, c = connect_to_db(db_name)
    volunteerName = input("Name:\n")
    print_general_volunteer_details(c, volunteerName)
    positions = ["mysecs"]
    for position in positions:
        print_position_details(c, volunteerName, position)
    deconnect_from_db(conn)


def print_general_volunteer_details(c, volunteerName):
    c.execute("SELECT * FROM volunteers WHERE volunteerName = '{}'"
              .format(volunteerName))
    _, gender, birthDate = c.fetchall()[0]
    print("Gender: {}".format(gender))
    print("Birth date: {}".format(birthDate))


def print_position_details(c, volunteerName, position):
    c.execute("SELECT * FROM {} WHERE volunteerName = '{}'"
              .format(position, volunteerName))
    _, regionName, startDate, endDate = c.fetchall()[0]
    print("Region: {}".format(regionName))
    print("Start date: {}".format(startDate))
    print("End date: {}".format(endDate))


if __name__ == '__main__':
    print_all_volunteer_details("MY-Ko.db")
