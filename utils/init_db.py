import sqlite3
import csv
import os


def init_db(data_path, db_name):
    conn, c = connect_to_db(db_name)
    drop_old_tables(c)
    create_all_tables(c)
    populate_all_tables(data_path, c)
    deconnect_from_db(conn)


def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn, conn.cursor()


def drop_old_tables(c):
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in c.fetchall():
        c.execute("DROP TABLE IF EXISTS {}".format(table[0]))


def create_all_tables(c):
    create_table_weekends(c)
    create_table_participants(c)
    create_table_weekend_participant(c)


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


def populate_all_tables(data_path, c):
    populate_table_weekends(data_path, c)
    populate_table_participants_and_table_weekend_participant(data_path, c)


def populate_table_weekends(data_path, c):
    for weekend_base_info in read_base_info_weekends(
            data_path):
        add_entry_to_table_weekends(c, weekend_base_info)


def read_base_info_weekends(data_path):
    with open("{}/weekends.txt".format(
            data_path),
            "r") as all_weekend_file:
        all_weekend_file.readline()
        result = all_weekend_file.readlines()
    return result


def add_entry_to_table_weekends(c, weekend_base_info):
    c.execute(
        "INSERT INTO weekends VALUES ({})".format(weekend_base_info))


def populate_table_participants_and_table_weekend_participant(
        data_path, c):
    for weekend_file_name, weekend_id in get_weekend_file_names_and_ids(c):
        with open("{}/participants/{}".format(
                data_path, weekend_file_name),
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


def add_entry_to_table_participants(c, participant_info):
    c.execute(
        """INSERT OR REPLACE INTO participants
            VALUES ('{}', '{}', '{}', '{}', '{}')""".format(
                *extract_full_participant_info_from_csv_row(participant_info)))


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


def deconnect_from_db(conn):
    conn.commit()
    conn.close()


if __name__ == '__main__':
    data_path = "{}/data".format(get_relative_path_to_script())
    init_db(data_path, "Weekend.db")
