import sqlite3
import csv
import os


def init_db(all_weekends_file_name, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    drop_old_tables(c)
    create_table_weekends(c)
    create_table_participants(c)
    create_table_weekend_participant(c)
    relative_path = get_relative_path_to_script()
    for weekend_base_info in read_base_info_weekends(
            relative_path, all_weekends_file_name):
        c.execute(
            "INSERT INTO weekends VALUES ({})".format(weekend_base_info))
    # Obtains the file names for all CSVs containing the weekend participants
    # together with the corresponding weekendIds.
    c.execute(
        "SELECT startDate || '_' ||name || '.csv', weekendId from weekends")
    weekend_file_infos = c.fetchall()
    # Iterates of all participant CSV
    for weekend_file_info in weekend_file_infos:
        with open("{}/data/participants/{}".format(
                relative_path, weekend_file_info[0]),
                encoding='latin1') as CSV_file:
            csv_reader = csv.reader(CSV_file, delimiter=",")
            next(csv_reader)
            for row in csv_reader:
                participantName = row[8]
                membershipNr = row[0]
                status = row[1]
                gender = row[9]
                birthDate = YYYYMMDD_from_DDMMYYY(row[10])
                # Adds participant or replaces entry if participant is already
                # in the participants table.
                c.execute(
                    """INSERT OR REPLACE INTO participants
                        VALUES ('{}', '{}', '{}', '{}', '{}')""".format(
                            participantName, membershipNr,
                            status, gender, birthDate))
                # Adds participantName and weekendId as foreign keys to the
                # weekend_participant table.
                c.execute(
                    """INSERT INTO weekend_participant
                        VALUES ('{}', '{}')""".format(
                            weekend_file_info[1], participantName))
    conn.commit()
    conn.close()


def drop_old_tables(c):
    c.execute("DROP TABLE IF EXISTS weekends")
    c.execute("DROP TABLE IF EXISTS participants")
    c.execute("DROP TABLE IF EXISTS weekend_participant")


def create_table_weekends(c):
    c.execute(
        """CREATE TABLE weekends (
            weekendId integer PRIMARY KEY NOT NULL,
            name text NOT NULL,
            location text NOT NULL,
            startDate date NOT NULL,
            endDate date NOT NULL);""")


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


def get_relative_path_to_script():
    return os.path.dirname(os.path.abspath(__file__))


def read_base_info_weekends(relative_path, all_weekends_file_name):
    with open("{}/data/{}".format(
            relative_path, all_weekends_file_name),
            "r") as all_weekend_file:
        all_weekend_file.readline()
        result = all_weekend_file.readlines()
    return result


def YYYYMMDD_from_DDMMYYY(date_string):
    return "-".join(date_string.split(".")[::-1])


init_db("weekends.txt", "Weekend.db")
