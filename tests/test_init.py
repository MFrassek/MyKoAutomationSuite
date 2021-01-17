import unittest
import os
from utils import init_db
import sqlite3
from utils import helper


class TestDbInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDbInitiation, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test_init.db"

    def setUp(self):
        self.conn, self.c = helper.connect_to_db(self.db_name)

    def tearDown(self):
        helper.uncommited_disconnect_from_db(self.conn)

    def test_weekend_file_exists(self):
        self.assertTrue(
            os.path.exists("{}/weekends.txt".format(self.data_path)),
            "weekends.txt does not exist at expected location")

    def test_connects_to_db(self):
        self.assertIsInstance(self.conn, sqlite3.Connection)
        self.assertIsInstance(self.c, sqlite3.Cursor)

    def test_initilization_components_successful(self):
        init_db.drop_old_tables(self.c)
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.assertEqual(self.c.fetchall(), [])
        init_db.create_all_tables(self.c)
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.assertEqual(
            self.c.fetchall(),
            [('weekends',), ('participants',), ('weekend_participant',),
             ('regions',), ('volunteers',), ('mysecs',)])


if __name__ == '__main__':
    unittest.main()
