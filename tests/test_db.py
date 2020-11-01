import unittest
import os
from utils import init_db
import sqlite3
from utils import helper


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
        helper.disconnect_from_db(self.conn)

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
        init_db.populate_all_tables(self.data_path, self.c)
        self.c.execute("SELECT COUNT(*) FROM weekends")
        self.assertEqual(self.c.fetchall(), [(2,)])
        self.c.execute("SELECT COUNT(*) FROM participants")
        self.assertEqual(self.c.fetchall(), [(5,)])
        self.c.execute("SELECT COUNT(*) FROM weekend_participant")
        self.assertEqual(self.c.fetchall(), [(8,)])
        self.c.execute("SELECT COUNT(*) FROM regions")
        self.assertEqual(self.c.fetchall(), [(40,)])

    def test_adding_entry(self):
        init_db.init_db(self.data_path, self.db_name)
        init_db.add_entry_to_table_participants(
            self.c, ["0000000009", "Wohnhaft in Deutschland", "10.01.2018", "",
                     "Zoe", "", "Zoes", "Zoes, Zoe", "Zoe Zoes", "f",
                     "05.04.1989", "31", "", "", "", "", "", "", "",
                     "Albertlane 5", "10000", "Alberta", "", "Frau", 0, "Ja",
                     "", "", "", "049", "", "Frankfurt"])
        self.c.execute("""SELECT COUNT(participantName) FROM participants
            WHERE participantName == 'Zoe Zoes'""")
        self.assertEqual(self.c.fetchall(), [(1,)])
        init_db.add_entry_to_table_weekend_participant(
            self.c, ["0000000009", "Wohnhaft in Deutschland", "10.01.2018", "",
                     "Zoe", "", "Zoes", "Zoes, Zoe", "Zoe Zoes", "f",
                     "05.04.1989", "31", "", "", "", "", "", "", "",
                     "Albertlane 5", "10000", "Alberta", "", "Frau", 0, "Ja",
                     "", "", "", "049", "", "Frankfurt"], 10)
        self.c.execute("""SELECT COUNT(participantName)
            FROM weekend_participant
            WHERE participantName == 'Zoe Zoes'""")
        self.assertEqual(self.c.fetchall(), [(1,)])
        init_db.add_entry_to_table_weekends(
            self.c, "20, 'Name5', 'Place5', '2020-01-10',\
            '2020-01-14', 'Münster'")
        self.c.execute("""SELECT COUNT(location)
            FROM weekends
            WHERE location == 'Place5'""")
        self.assertEqual(self.c.fetchall(), [(1,)])


if __name__ == '__main__':
    unittest.main()
