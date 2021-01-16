import unittest
import os
from utils import userPrompt
from utils.userPrompt import UserPrompt


class TestInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInitiation, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test.db"

    def setUp(self):
        pass

    def tearDown(self):
        userPrompt.input = input

    def test_prompts(self):
        generator = (ele for ele in
                     ["1NotVolunteerName", "Frank Test",
                      "x", "f",
                      "11.11.1990", "1990-11-11",
                      "MYSec",
                      "1Münster", "Münster",
                      "11-11-2020", "2020-11-11",
                      "March 11th, 2021", "2021-03-11",
                      "A", "1",
                      ""])
        userPrompt.input = lambda x: next(generator)
        volunteer_name = UserPrompt.get_volunteer_name()
        self.assertEqual(volunteer_name, "Frank Test")
        gender = UserPrompt.get_gender()
        self.assertEqual(gender, "f")
        birth_date = UserPrompt.get_birth_date()
        self.assertEqual(birth_date, "1990-11-11")
        position_names = UserPrompt.get_position_names()
        self.assertEqual(position_names, ["MYSec"])
        region_name = UserPrompt.get_region_name()
        self.assertEqual(region_name, "Münster")
        start_date = UserPrompt.get_start_date()
        self.assertEqual(start_date, "2020-11-11")
        end_date = UserPrompt.get_end_date()
        self.assertEqual(end_date, "2021-03-11")
        position_id = UserPrompt.get_position_id()
        self.assertEqual(position_id, "1")
