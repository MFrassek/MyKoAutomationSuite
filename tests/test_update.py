import unittest
from utils import volunteer_update_position
import databaseConnection
from _pytest.monkeypatch import MonkeyPatch


class TestUpdate(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUpdate, self).__init__(*args, **kwargs)
        self.db_name = "tests/TestFilled.db"

    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.monkeypatch.setattr(
            "databaseConnection.DatabaseConnection.db_name", self.db_name)
        self.monkeypatch.setattr(
            "databaseConnection.DatabaseConnection.commit", lambda x: None)

    def tearDown(self):
        databaseConnection.DatabaseConnection.close()
        self.monkeypatch.undo()

    def test_update_position(self):
        generator = (ele for ele in ["Test Person", "2021-01-17"])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        volunteer_update_position.update_position()
        position = volunteer_update_position\
            .Position.create_all_held_positions("Test Person")[0]
        self.assertEqual(position.end_date, "2021-01-17")
