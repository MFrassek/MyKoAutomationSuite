import sqlite3
import os


def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn, conn.cursor()


def deconnect_from_db(conn):
    conn.commit()
    conn.close()


def get_relative_path_to_script():
    return os.path.dirname(os.path.abspath(__file__))