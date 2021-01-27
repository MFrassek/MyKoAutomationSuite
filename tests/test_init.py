import unittest
from utils import init_db
import databaseConnection
from _pytest.monkeypatch import MonkeyPatch


class TestDbInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDbInitiation, self).__init__(*args, **kwargs)
        self.db_name = "tests/TestEmpty.db"

    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.monkeypatch.setattr(
            "databaseConnection.DatabaseConnection.db_name", self.db_name)
        self.monkeypatch.setattr(
            "databaseConnection.DatabaseConnection.commit", lambda x: None)

    def tearDown(self):
        databaseConnection.DatabaseConnection.close()
        self.monkeypatch.undo()

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
