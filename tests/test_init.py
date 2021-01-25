import unittest
import os
from utils import init_db
import databaseConnection
from _pytest.monkeypatch import MonkeyPatch


class TestDbInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDbInitiation, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test.db"

    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.monkeypatch.setattr(
            "databaseConnection.DatabaseConnection.db_name", self.db_name)

    def tearDown(self):
        self.monkeypatch.undo()
        databaseConnection.DatabaseConnection.close()

    def test_weekend_file_exists(self):
        self.assertTrue(
            os.path.exists("{}/Weekends.txt".format(self.data_path)),
            "Weekends.txt does not exist at expected location")

    def test_initilization_components_successful(self):
        init_db.drop_old_tables()
        self.assertEqual(databaseConnection.DatabaseConnection().query(
            "SELECT name FROM sqlite_master WHERE type='table';"), [])
        init_db.create_all_tables()
        self.assertEqual(databaseConnection.DatabaseConnection().query(
            "SELECT name FROM sqlite_master WHERE type='table';"),
            [('weekends',), ('participants',), ('weekend_participant',),
             ('regions',), ('volunteers',), ('mysecs',)])


if __name__ == '__main__':
    unittest.main()
