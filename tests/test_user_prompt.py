import unittest
import os
from utils import userPrompt
from utils.userPrompt import UserPrompt
from _pytest.monkeypatch import MonkeyPatch


class TestUserPrompt(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUserPrompt, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test.db"

    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    def tearDown(self):
        self.monkeypatch.undo()

    def test_prompting_volunteer_name(self):
        generator = (ele for ele in ["1NotVolunteerName", "Frank Test", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        volunteer_name = UserPrompt.get_volunteer_name()
        self.assertEqual(volunteer_name, "Frank Test")

    def test_prompting_gender(self):
        generator = (ele for ele in ["x", "f", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        gender = UserPrompt.get_gender()
        self.assertEqual(gender, "f")

    def test_prompting_birth_date(self):
        generator = (ele for ele in ["11.11.1990", "1990-11-11", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        birth_date = UserPrompt.get_birth_date()
        self.assertEqual(birth_date, "1990-11-11")

    def test_prompting_position_name(self):
        generator = (ele for ele in ["MYSec"])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        position_names = UserPrompt.get_position_names()
        self.assertEqual(position_names, ["MYSec"])

    def test_prompting_region_name(self):
        generator = (ele for ele in ["1Münster", "Münster", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        region_name = UserPrompt.get_region_name()
        self.assertEqual(region_name, "Münster")

    def test_prompting_start_date(self):
        generator = (ele for ele in ["11-11-2020", "2020-11-11", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        start_date = UserPrompt.get_start_date()
        self.assertEqual(start_date, "2020-11-11")

    def test_prompting_end_date(self):
        generator = (ele for ele in ["March 11th, 2021", "2021-03-11", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        end_date = UserPrompt.get_end_date()
        self.assertEqual(end_date, "2021-03-11")

    def test_prompting_position_id(self):
        generator = (ele for ele in ["A", "1", ""])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        position_id = UserPrompt.get_position_id()
        self.assertEqual(position_id, "1")
