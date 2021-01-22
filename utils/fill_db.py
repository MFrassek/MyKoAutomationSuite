from helper import connect_to_db, disconnect_from_db, \
    get_relative_path_to_script
import csv
from regionPopulator import RegionPopulator
from volunteerPopulator import VolunteerPopulator
from positionPopulator import PositionPopulator
from weekendPopulator import WeekendPopulator


def fill_db(data_path, db_name):
    conn, c = connect_to_db(db_name)
    populate_all_tables(data_path, c)
    disconnect_from_db(conn)
    RegionPopulator.populate_table()
    VolunteerPopulator.populate_table()
    PositionPopulator.populate_table()
    WeekendPopulator.populate_table()


def populate_all_tables(data_path, c):
    populate_table_participants_and_table_weekend_participant(data_path, c)


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
        "SELECT startDate || '_' || weekendName || '.csv', weekendId from weekends")
    return c.fetchall()


def add_entry_to_table_participants(c, participant_info):
    c.execute(
        """INSERT OR REPLACE INTO participants
            VALUES ('{}', '{}', '{}')""".format(
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


if __name__ == '__main__':
    data_path = "{}/data".format(get_relative_path_to_script())
    fill_db(data_path, "MY-Ko.db")
