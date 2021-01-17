import sqlite3
import os


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
