import unittest
import databaseConnection
from utils.position import Position
from _pytest.monkeypatch import MonkeyPatch
from utils import init_db


class TestPosition(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPosition, self).__init__(*args, **kwargs)
        self.db_name = "tests/Test.db"

    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.monkeypatch.setattr(
            "databaseConnection.DatabaseConnection.db_name", self.db_name)
        init_db.init_db()
        Position("MYSec", "Hamburg", "Test Person", "2020-03-02").add_to_db()
        Position("MYSec", "München", "Second Person", "2021-01-02").add_to_db()

    def tearDown(self):
        self.monkeypatch.undo()
        databaseConnection.DatabaseConnection.close()

    def test_position_accessibility(self):
        pos = Position(
            title="MYSec", region="Münster", held_by="Other Person",
            start_date="2019-12-12")
        self.assertEqual(pos.title, "MYSec")
        self.assertEqual(pos.region, "Münster")
        self.assertEqual(pos.held_by, "Other Person")
        self.assertEqual(pos.start_date, "2019-12-12")
        self.assertEqual(pos.end_date, "")

    def test_position_mutability(self):
        pos = Position(
            title="MYSec", region="Münster", held_by="Other Person",
            start_date="2019-12-12")
        pos.end_date = "2019-12-13"
        self.assertEqual(pos.end_date, "2019-12-13")
        with self.assertRaises(AttributeError):
            pos.title = "New"
        with self.assertRaises(AttributeError):
            pos.region = "New"
        with self.assertRaises(AttributeError):
            pos.held_by = "New"
        with self.assertRaises(AttributeError):
            pos.start_date = "0001-01-01"

    def test_position_equal(self):
        self.assertEqual(
            Position("MYSec", "Münster", "Other Person", "2019-12-12"),
            Position("MYSec", "Münster", "Other Person", "2019-12-12"))
        self.assertNotEqual(
            Position("MYSec", "Münster", "Other Person", "2019-12-12"),
            Position("MYSec", "Thüringen", "Other Person", "2019-12-12"))

    def test_position_hash(self):
        self.assertEqual(
            hash(Position("MYSec", "Münster", "Other Person", "2019-12-12")),
            hash(Position("MYSec", "Münster", "Other Person", "2019-12-12")))
        self.assertNotEqual(
            hash(Position("MYSec", "Münster", "Other Person", "2019-12-12")),
            hash(Position("MYSec", "Thüringen", "Other Person", "2019-12-12")))

    def test_position_factory_methods(self):
        self.assertEqual(len(Position.create_all(title="MYSec")), 2)
        self.assertEqual(len(Position.create_all_fitting_data(
            [["start_date", ">", "2020-12-12"]], title="MYSec")), 1)
        self.assertEqual(
            len(Position.create_all_held_positions("Test Person")), 1)

    def test_get_details_fitting_data(self):
        self.assertEqual(
            Position.get_details_fitting_data(
                [["end_date", "=", ""]], title="MYSec"),
            [(1, "Test Person", "Hamburg", "2020-03-02", ""),
             (2, "Second Person", "München", "2021-01-02", "")])

    def test_update_db(self):
        pos = Position.create_all_held_positions("Test Person")[0]
        original_end_date = pos.end_date
        pos.end_date = "2021-01-18"
        pos.update_in_db()
        pos = Position.create_all_held_positions("Test Person")[0]
        new_end_date = pos.end_date
        self.assertNotEqual(original_end_date, new_end_date)
