import sqlite3
import os
import re


def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn, conn.cursor()


def disconnect_from_db(conn):
    conn.commit()
    conn.close()


def uncommited_disconnect_from_db(conn):
    conn.close()


def get_relative_path_to_script():
    return os.path.dirname(os.path.abspath(__file__))


def get_general_volunteer_details(c, volunteerName):
    c.execute("SELECT * FROM volunteers WHERE volunteerName = '{}'"
              .format(volunteerName))
    return c.fetchall()[0]


def get_position_details(c, volunteerName, position):
    c.execute("SELECT * FROM {} WHERE volunteerName = '{}'"
              .format(position, volunteerName))
    return c.fetchall()[0]


def string_follows_input_pattern(string, data_type):
    data_type_patterns = {
        "name": r"^[a-üA-Ü, -]+$",
        "date": r"^\d\d\d\d-\d\d-\d\d$",
        "gender": r"^[mfdu]$",
        "id": r"\d+"}
    return string == "" or re.match(data_type_patterns[data_type], string)


def get_data_type_from_column_name(column_name):
    if column_name.endswith("Name"):
        return "name"
    elif column_name.endswith("Date"):
        return "date"
    elif column_name.endswith("gender"):
        return "gender"
