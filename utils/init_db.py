from helper import connect_to_db, disconnect_from_db,\
    get_relative_path_to_script


def init_db(data_path, db_name):
    conn, c = connect_to_db(db_name)
    drop_old_tables(c)
    create_all_tables(c)
    disconnect_from_db(conn)


def drop_old_tables(c):
    for table in get_all_existing_table_names(c):
        c.execute("DROP TABLE IF EXISTS {}".format(table))


def get_all_existing_table_names(c):
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [table_tuple[0] for table_tuple in c.fetchall()]


def create_all_tables(c):
    create_table_weekends(c)
    create_table_participants(c)
    create_table_weekend_participant(c)
    create_table_regions(c)
    create_table_volunteers(c)
    create_table_mysecs(c)


def create_table_weekends(c):
    c.execute(
        """CREATE TABLE weekends (
            weekendId integer PRIMARY KEY NOT NULL,
            name text NOT NULL,
            location text NOT NULL,
            startDate date NOT NULL,
            endDate date NOT NULL,
            regionName text NOT NULL);""")


def create_table_participants(c):
    c.execute(
        """CREATE TABLE participants (
            participantName text PRIMARY KEY NOT NULL,
            membershipNr integer DEFAULT 0,
            status text NOT NULL,
            gender text NOT NULL,
            birthDate date NOT NULL);""")


def create_table_weekend_participant(c):
    c.execute(
        """CREATE TABLE weekend_participant (
            weekendId integer NOT NULL,
            participantName text NOT NULL);""")


def create_table_regions(c):
    c.execute(
        """CREATE TABLE regions (
            regionId integer NOT NULL,
            regionName text PRIMARY KEY NOT NULL,
            regionMailName text NOT NULL,
            magazineName text NOT NULL,
            mCount integer NOT NULL,
            myCount integer NOT NULL,
            looking boolean NOT NULL);""")


def create_table_volunteers(c):
    c.execute(
        """CREATE TABLE volunteers(
            volunteerName text PRIMARY KEY NOT NULL,
            gender text NOT NULL,
            birthDate date NOT NULL);""")


def create_table_mysecs(c):
    c.execute(
        """CREATE TABLE mysecs(
            positionId integer PRIMARY KEY NOT NULL,
            volunteerName text NOT NULL,
            regionName text NOT NULL,
            startDate date NOT NULL,
            endDate date);""")


if __name__ == '__main__':
    data_path = "{}/data".format(get_relative_path_to_script())
    init_db(data_path, "MY-Ko.db")
