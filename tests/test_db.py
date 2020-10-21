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
        self.assertIsInstance(self.c, sqlite3.Cursor)

    def test_initilization_components_successful(self):
        init_db.drop_old_tables(self.c)
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.assertEqual(self.c.fetchall(), [])
        init_db.create_all_tables(self.c)
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.assertEqual(
            self.c.fetchall(),
            [('weekends',), ('participants',), ('weekend_participant',)])
        init_db.populate_all_tables(self.data_path, self.c)
        self.c.execute("SELECT COUNT(*) FROM weekends")
        self.assertEqual(self.c.fetchall(), [(2,)])
        self.c.execute("SELECT COUNT(*) FROM participants")
        self.assertEqual(self.c.fetchall(), [(5,)])
        self.c.execute("SELECT COUNT(*) FROM weekend_participant")
        self.assertEqual(self.c.fetchall(), [(8,)])


if __name__ == '__main__':
    unittest.main()
