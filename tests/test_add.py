import unittest
import os
import databaseConnection
from utils import volunteer_add
from utils import init_db
from _pytest.monkeypatch import MonkeyPatch


class TestAdd(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAdd, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test.db"

    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.monkeypatch.setattr(
            "databaseConnection.DatabaseConnection.db_name", self.db_name)
        init_db.init_db(self.data_path)

    def tearDown(self):
        self.monkeypatch.undo()
        databaseConnection.DatabaseConnection.close()

    def test_add_volunteer(self):
        generator = (ele for ele in ["1995-03-03", "d"])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        volunteer_add.add_new_volunteer("Test Person")
        self.assertEqual(len(volunteer_add.Volunteer.create_all()), 1)

    def test_add_mysec(self):
        generator = (ele for ele in ["Münster", "2020-01-01", "", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        volunteer_add.add_new_position("MYSec", "Test Person")
        self.assertEqual(
            len(volunteer_add.Position.create_all(title="MYSec")), 1)
