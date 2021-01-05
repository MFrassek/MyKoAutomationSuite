from helper import connect_to_db, disconnect_from_db, \
    get_relative_path_to_script
import csv


def fill_db(data_path, db_name):
    conn, c = connect_to_db(db_name)
    populate_all_tables(data_path, c)
    disconnect_from_db(conn)


def populate_all_tables(data_path, c):
    populate_table_weekends(data_path, c)
    populate_table_participants_and_table_weekend_participant(data_path, c)
    populate_table_regions(data_path, c)


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


def populate_table_regions(data_path, c):
    for region_info in read_info_regions(data_path):
        add_entry_to_table_region(c, region_info)


def read_info_regions(data_path):
    with open("{}/LocSecRegions.txt".format(data_path), "r")\
            as all_region_file:
        result = all_region_file.readlines()
    return result


def add_entry_to_table_region(c, region_info):
    c.execute(
        "INSERT INTO regions VALUES ({}, True)".format(region_info))


if __name__ == '__main__':
    data_path = "{}/data".format(get_relative_path_to_script())
    fill_db(data_path, "MY-Ko.db")
