import unittest
import os
import databaseConnection
from utils import volunteer_update_position
from utils import volunteer_add
from utils import init_db
from _pytest.monkeypatch import MonkeyPatch


class TestUpdate(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUpdate, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test.db"

    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        generator = (ele for ele in ["Münster", "2020-01-01", "", ""])
        self.monkeypatch.setattr(
            "databaseConnection.DatabaseConnection.db_name", self.db_name)
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        init_db.init_db(self.data_path)
        volunteer_add.add_new_position("MYSec", "Test Person")

    def tearDown(self):
        self.monkeypatch.undo()
        databaseConnection.DatabaseConnection.close()

    def test_update_position(self):
        generator = (ele for ele in ["Test Person", "2021-01-17"])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        volunteer_update_position.update_position()
        position = volunteer_update_position\
            .Position.create_all_held_positions("Test Person")[0]
        self.assertEqual(position.end_date, "2021-01-17")
