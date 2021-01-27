from databaseConnection import DatabaseConnection


def init_db():
    drop_old_tables()
    create_all_tables()


def drop_old_tables():
    for table in get_all_existing_table_names():
        DatabaseConnection().change("DROP TABLE IF EXISTS {}".format(table))


def get_all_existing_table_names():
    return [table_tuple[0] for table_tuple
            in DatabaseConnection().query(
            "SELECT name FROM sqlite_master WHERE type='table';")]


def create_all_tables():
    create_table_weekends()
    create_table_participants()
    create_table_weekend_participant()
    create_table_regions()
    create_table_volunteers()
    create_table_mysecs()


def create_table_weekends():
    DatabaseConnection().change(
        """CREATE TABLE weekends (
            weekendId integer PRIMARY KEY NOT NULL,
            weekendName text NOT NULL,
            weekendLocation text NOT NULL,
            startDate date NOT NULL,
            endDate date NOT NULL,
            regionName text NOT NULL);""")


def create_table_participants():
    DatabaseConnection().change(
        """CREATE TABLE participants (
            personName text PRIMARY KEY NOT NULL,
            gender text NOT NULL,
            birthDate date NOT NULL);""")


def create_table_weekend_participant():
    DatabaseConnection().change(
        """CREATE TABLE weekend_participant (
            weekendId integer NOT NULL,
            personName text NOT NULL);""")


def create_table_regions():
    DatabaseConnection().change(
        """CREATE TABLE regions (
            regionId integer NOT NULL,
            regionName text PRIMARY KEY NOT NULL,
            regionMailName text NOT NULL,
            magazineName text NOT NULL,
            mCount integer NOT NULL,
            myCount integer NOT NULL,
            looking boolean NOT NULL);""")


def create_table_volunteers():
    DatabaseConnection().change(
        """CREATE TABLE volunteers(
            personName text PRIMARY KEY NOT NULL,
            gender text NOT NULL,
            birthDate date NOT NULL);""")


def create_table_mysecs():
    DatabaseConnection().change(
        """CREATE TABLE mysecs(
            positionId integer PRIMARY KEY NOT NULL,
            personName text NOT NULL,
            regionName text NOT NULL,
            startDate date NOT NULL,
            endDate date);""")


if __name__ == '__main__':
    init_db()
    DatabaseConnection.close()
