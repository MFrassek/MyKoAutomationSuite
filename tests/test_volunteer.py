import unittest
import os
import databaseConnection
from utils.person import Volunteer
from utils.position import Position
from _pytest.monkeypatch import MonkeyPatch
from utils import init_db


class TestVolunteer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestVolunteer, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test.db"

    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.monkeypatch.setattr(
            "databaseConnection.DatabaseConnection.db_name", self.db_name)
        init_db.init_db(self.data_path, self.db_name)
        Position("MYSec", "Kiel", "Test Person", "2020-04-04", "").add_to_db()
        Volunteer("Test Person", "u", "1994-07-05").add_to_db()

    def tearDown(self):
        self.monkeypatch.undo()
        databaseConnection.DatabaseConnection.close()

    def test_volunteer_accessibility(self):
        vol = Volunteer(
            name="Test Person", gender="u",
            birth_date="1994-07-05")
        self.assertEqual(vol.name, "Test Person")
        self.assertEqual(vol.gender, "u")
        self.assertEqual(vol.birth_date, "1994-07-05")
        self.assertEqual(vol.positions[0].title, "MYSec")
        self.assertEqual(vol.positions[0].held_by, "Test Person")
        self.assertEqual(vol.positions[0].region, "Kiel")
        self.assertEqual(vol.positions[0].start_date, "2020-04-04")
        self.assertEqual(vol.positions[0].end_date, "")

    def test_volunteer_mutability(self):
        vol = Volunteer(
            name="Test Person", gender="u",
            birth_date="1994-07-05")
        with self.assertRaises(AttributeError):
            vol.name = "New Name"
        with self.assertRaises(AttributeError):
            vol.gender = "New"
        with self.assertRaises(AttributeError):
            vol.birth_date = "0001-01-01"
        with self.assertRaises(AttributeError):
            vol.positions = ("New Position")

    def test_volunteer_equal(self):
        self.assertEqual(
            Volunteer(name="Test Person", gender="u", birth_date="1994-07-05"),
            Volunteer(name="Test Person", gender="u", birth_date="1994-07-05"))
        self.assertNotEqual(
            Volunteer(name="Test Person", gender="u", birth_date="1994-07-05"),
            Volunteer(name="Test Verson", gender="u", birth_date="1994-07-05"))

    def test_volunteer_hash(self):
        self.assertEqual(
            hash(Volunteer(name="Test Person", gender="u", birth_date="1994-07-05")),
            hash(Volunteer(name="Test Person", gender="u", birth_date="1994-07-05")))
        self.assertNotEqual(
            hash(Volunteer(name="Test Person", gender="u", birth_date="1994-07-05")),
            hash(Volunteer(name="Test Verson", gender="u", birth_date="1994-07-05")))

    def test_volunteer_factory_methods(self):
        self.assertEqual(len(Volunteer.create_all()), 1)
        self.assertEqual(len(Volunteer.create_all_fitting_data(
            [["name", "=", "Test Person"]])), 1)

    def test_get_details_fitting_data(self):
        self.assertEqual(
            Volunteer.get_details_fitting_data([["name", "=", "Test Person"]]),
            [("Test Person", "u", "1994-07-05")])
