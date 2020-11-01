from helper import connect_to_db, disconnect_from_db,\
    get_general_volunteer_details, get_position_details


def print_all_volunteer_details(db_name):
    conn, c = connect_to_db(db_name)
    volunteerName = input("Name:\n")
    print_general_volunteer_details(c, volunteerName)
    positions = ["mysecs"]
    for position in positions:
        print_position_details(c, volunteerName, position)
    disconnect_from_db(conn)


def print_general_volunteer_details(c, volunteerName):
    _, gender, birthDate = get_general_volunteer_details(c, volunteerName)
    print("Gender: {}".format(gender))
    print("Birth date: {}".format(birthDate))


def print_position_details(c, volunteerName, position):
    _, regionName, startDate, endDate = \
        get_position_details(c, volunteerName, position)
    print("Region: {}".format(regionName))
    print("Start date: {}".format(startDate))
    print("End date: {}".format(endDate))


if __name__ == '__main__':
    print_all_volunteer_details("MY-Ko.db")
