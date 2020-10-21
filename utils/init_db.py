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
    populate_table_weekends(relative_path, all_weekends_file_name, c)
    populate_table_participants_and_table_weekend_participant(relative_path, c)
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


def populate_table_weekends(relative_path, all_weekends_file_name, c):
    for weekend_base_info in read_base_info_weekends(
            relative_path, all_weekends_file_name):
        c.execute(
            "INSERT INTO weekends VALUES ({})".format(weekend_base_info))


def read_base_info_weekends(relative_path, all_weekends_file_name):
    with open("{}/data/{}".format(
            relative_path, all_weekends_file_name),
            "r") as all_weekend_file:
        all_weekend_file.readline()
        result = all_weekend_file.readlines()
    return result


def populate_table_participants_and_table_weekend_participant(
        relative_path, c):
    for weekend_file_name, weekend_id in get_weekend_file_names_and_ids(c):
        with open("{}/data/participants/{}".format(
                relative_path, weekend_file_name),
                encoding='latin1') as CSV_file:
            participant_infos = csv.reader(CSV_file, delimiter=",")
            next(participant_infos)
            for participant_info in participant_infos:
                add_entry_to_table_participants(c, participant_info)
                add_entry_to_table_weekend_participant(
                    c, participant_info, weekend_id)


def get_weekend_file_names_and_ids(c):
    c.execute(
        "SELECT startDate || '_' ||name || '.csv', weekendId from weekends")
    return c.fetchall()


def add_entry_to_table_participants(c, row):
    c.execute(
        """INSERT OR REPLACE INTO participants
            VALUES ('{}', '{}', '{}', '{}', '{}')""".format(
                *extract_full_participant_info_from_csv_row(row)))


def extract_full_participant_info_from_csv_row(participant_info):
    participantName = extract_participant_name_from_csv_row(participant_info)
    membershipNr = participant_info[0]
    status = participant_info[1]
    gender = participant_info[9]
    birthDate = YYYYMMDD_from_DDMMYYY(participant_info[10])
    return participantName, membershipNr, status, gender, birthDate


def extract_participant_name_from_csv_row(participant_info):
    return participant_info[8]


def YYYYMMDD_from_DDMMYYY(date_string):
    return "-".join(date_string.split(".")[::-1])


def add_entry_to_table_weekend_participant(c, participant_info, weekend_id):
    c.execute(
        """INSERT INTO weekend_participant
            VALUES ('{}', '{}')""".format(
                weekend_id,
                extract_participant_name_from_csv_row(participant_info)))


init_db("weekends.txt", "Weekend.db")
