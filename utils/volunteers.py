import sqlite3


def add_new_volunteer_and_position(db_name):
    conn, c = connect_to_db(db_name)
    position_name = input("Position:\n")
    volunteerName = input("Name:\n")
    gender = input("Gender [f, m or d]:\n")
    birthDate = input("Birthdate [YYYY-MM-DD]:\n")
    add_entry_to_table_volunteers(c, volunteerName, gender, birthDate)
    deconnect_from_db(conn)


def add_entry_to_table_volunteers(c, volunteerName, gender, birthDate):
    c.execute(
        "INSERT INTO volunteers VALUES ('{}', '{}', '{}')"
        .format(volunteerName, gender, birthDate))


def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn, conn.cursor()


def deconnect_from_db(conn):
    conn.commit()
    conn.close()


if __name__ == '__main__':
    add_new_volunteer_and_position("Weekend.db")
