import unittest
import os
import databaseConnection
from utils.userInteraction import UserInteraction
from _pytest.monkeypatch import MonkeyPatch
from utils.person import Volunteer
from utils.position import Position
from utils.region import Region
from utils import init_db


class TestUserInteraction(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUserInteraction, self).__init__(*args, **kwargs)
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

    def test_prompting_volunteer_name(self):
        generator = (ele for ele in ["1NotVolunteerName", "Frank Test", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        volunteer_name = UserInteraction.get_volunteer_name()
        self.assertEqual(volunteer_name, "Frank Test")

    def test_prompting_gender(self):
        generator = (ele for ele in ["x", "f", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        gender = UserInteraction.get_gender()
        self.assertEqual(gender, "f")

    def test_prompting_birth_date(self):
        generator = (ele for ele in ["11.11.1990", "1990-11-11", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        birth_date = UserInteraction.get_birth_date()
        self.assertEqual(birth_date, "1990-11-11")

    def test_prompting_position_name(self):
        generator = (ele for ele in ["MYSec"])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        position_names = UserInteraction.get_position_names()
        self.assertEqual(position_names, ["MYSec"])

    def test_prompting_region_name(self):
        generator = (ele for ele in ["1Münster", "Münster", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        region_name = UserInteraction.get_region_name()
        self.assertEqual(region_name, "Münster")

    def test_prompting_start_date(self):
        generator = (ele for ele in ["11-11-2020", "2020-11-11", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        start_date = UserInteraction.get_start_date()
        self.assertEqual(start_date, "2020-11-11")

    def test_prompting_end_date(self):
        generator = (ele for ele in ["March 11th, 2021", "2021-03-11", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        end_date = UserInteraction.get_end_date()
        self.assertEqual(end_date, "2021-03-11")

    def test_prompting_position_id(self):
        generator = (ele for ele in ["A", "1", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        position_id = UserInteraction.get_position_id()
        self.assertEqual(position_id, "1")

    def test_post_volunteer(self):
        printed_statements = []
        self.monkeypatch.setattr(
            "builtins.print", lambda x: printed_statements.append(x))
        UserInteraction.post_volunteer_details(
            Volunteer("M M", "m", "1999-09-09"))
        self.assertEqual(
            printed_statements,
            ["Name: M M", "Gender: m", "Birth date: 1999-09-09", "Positions:"])

    def test_post_position(self):
        printed_statements = []
        self.monkeypatch.setattr(
            "builtins.print", lambda x: printed_statements.append(x))
        UserInteraction.post_position_details(
            Position("MYSec", "Sachsen", "M Q", "2019-03-30"))
        self.assertEqual(
            printed_statements,
            ["Title: MYSec", "Held by: M Q", "Region: Sachsen", "Start date: 2019-03-30", "End date: "])

    def test_post_region(self):
        printed_statements = []
        self.monkeypatch.setattr(
            "builtins.print", lambda x: printed_statements.append(x))
        UserInteraction.post_region_details(
            Region("1000", "Test", "test", "Testana", 1, 1, 1))
        self.assertEqual(
            printed_statements,
            ["Id: 1000", "Region name: Test", "Mail name: test",
             "Magazine name: Testana", "M Count: 1", "MY Count: 1",
             "Looking state: 1"])
