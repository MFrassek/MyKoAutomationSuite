import unittest
import os
from utils import init_db
import sqlite3


class TestInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInitiation, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "Test.db"
        self.conn, self.c = init_db.connect_to_db(self.db_name)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_weekend_file_exists(self):
        self.assertTrue(
            os.path.exists("{}/weekends.txt".format(self.data_path)),
            "weekends.txt does not exist at expected location")

    def test_connects_to_db(self):
        self.assertIsInstance(self.conn, sqlite3.Connection)

    def test_no_old_tables_left_after_table_drop(self):
        init_db.drop_old_tables(self.c)
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.assertEqual(self.c.fetchall(), [])

    def test_make_new_tables(self):
        init_db.create_all_tables(self.c)
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.assertEqual(
            self.c.fetchall(),
            [('weekends',), ('participants',), ('weekend_participant',)])


if __name__ == '__main__':
    unittest.main()
