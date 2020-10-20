import sqlite3
import csv


def init_db(all_weekends_file_name):
    conn = sqlite3.connect('Weekend.db')
    c = conn.cursor()
    # Drops old tables if already existing-
    c.execute("DROP TABLE IF EXISTS weekends")
    c.execute("DROP TABLE IF EXISTS weekend_participant")
    c.execute("DROP TABLE IF EXISTS participants")
    # Creates table for all weekends.
    c.execute(
        """CREATE TABLE weekends (
            weekendId integer PRIMARY KEY NOT NULL,
            name text NOT NULL,
            location text NOT NULL,
            startDate date NOT NULL,
            endDate date NOT NULL);""")
    # Creates table for all participants.
    c.execute(
        """CREATE TABLE participants (
            participantName text PRIMARY KEY NOT NULL,
            membershipNr integer DEFAULT 0,
            status text NOT NULL,
            gender text NOT NULL,
            birthDate date NOT NULL);""")
    # Creates join table for many-to-many relationship
    # between weekends and participants.
    c.execute(
        """CREATE TABLE weekend_participant (
            weekendId integer NOT NULL,
            participantName text NOT NULL);""")
    # Fills weekend table, based on input from the all_weekend_file.
    with open(all_weekends_file_name, "r") as all_weekend_file:
        weekend_lines = all_weekend_file.readlines()
        for weekend_line in weekend_lines[1:]:
            c.execute(
                "INSERT INTO weekends VALUES ({})".format(weekend_line))
    # Obtains the file names for all CSVs containing the weekend participants
    # together with the corresponding weekendIds.
    c.execute(
        "SELECT startDate || '_' ||name || '.csv', weekendId from weekends")
    weekend_file_infos = c.fetchall()
    # Iterates of all participant CSV
    for weekend_file_info in weekend_file_infos:
        with open("participants/{}".format(
                weekend_file_info[0]), encoding='latin1') as CSV_file:
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


def YYYYMMDD_from_DDMMYYY(date_string):
    return "-".join(date_string.split(".")[::-1])


init_db("weekends.txt")
