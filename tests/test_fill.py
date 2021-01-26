import unittest
import os
from utils import fill_db
from utils import init_db
import databaseConnection
from _pytest.monkeypatch import MonkeyPatch


class TestDbFill(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDbFill, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test.db"

    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.monkeypatch.setattr(
            "databaseConnection.DatabaseConnection.db_name", self.db_name)
        self.monkeypatch.setattr(
            "tablePopulator.TablePopulator.data_path", self.data_path)
        init_db.init_db(self.data_path)

    def tearDown(self):
        self.monkeypatch.undo()
        databaseConnection.DatabaseConnection.close()

    def test_populate_tables(self):
        fill_db.fill_db()
        self.assertEqual(
            databaseConnection.DatabaseConnection().query(
                "SELECT COUNT(*) FROM weekends"), [(2,)])
        self.assertEqual(
            databaseConnection.DatabaseConnection().query(
                "SELECT COUNT(*) FROM participants"), [(5,)])
        self.assertEqual(
            databaseConnection.DatabaseConnection().query(
                "SELECT COUNT(*) FROM weekend_participant"), [(8,)])
        self.assertEqual(
            databaseConnection.DatabaseConnection().query(
                "SELECT COUNT(*) FROM regions"), [(40,)])
