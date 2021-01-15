import unittest
import os
from utils import volunteer_add
from utils import helper


class TestInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInitiation, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test.db"

    def setUp(self):
        volunteer_add.Position.db_name = self.db_name
        volunteer_add.Volunteer.db_name = self.db_name

    def tearDown(self):
        volunteer_add.input = input

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
        volunteer_add.input = lambda x: next(generator)
        volunteer_name = volunteer_add.prompt_volunteer_name()
        self.assertEqual(volunteer_name, "Frank Test")
        gender = volunteer_add.prompt_gender()
        self.assertEqual(gender, "f")
        birth_date = volunteer_add.prompt_birth_date()
        self.assertEqual(birth_date, "1990-11-11")
        position_names = volunteer_add.prompt_position_names()
        self.assertEqual(position_names, ["MYSec"])
        region_name = volunteer_add.prompt_region_name()
        self.assertEqual(region_name, "Münster")
        start_date = volunteer_add.prompt_start_date()
        self.assertEqual(start_date, "2020-11-11")
        end_date = volunteer_add.prompt_end_date()
        self.assertEqual(end_date, "2021-03-11")
        position_id = volunteer_add.prompt_position_id()
        self.assertEqual(position_id, "1")

    def test_add_entry_to_volunteers(self):
        container_prompt_gender_and_birthDate = \
            volunteer_add.prompt_gender_and_birthDate
        volunteer_add.prompt_gender_and_birthDate = lambda: ("m", "1992-10-01")
        volunteer_add.add_entry_to_table_volunteers(self.c, "Max Mustermann")
        self.c.execute("SELECT * FROM volunteers WHERE volunteerName = '{}'"
                       .format("Max Mustermann"))
        volunteerName, gender, birthDate = self.c.fetchall()[0]
        volunteer_add.prompt_gender_and_birthDate = \
            container_prompt_gender_and_birthDate
        self.assertEqual(volunteerName, "Max Mustermann")
        self.assertEqual(gender, "m")
        self.assertEqual(birthDate, "1992-10-01")

    def test_add_entry_to_mysecs(self):
        container_prompt_regionName_and_startDate = \
            volunteer_add.prompt_regionName_and_startDate
        volunteer_add.prompt_regionName_and_startDate = \
            lambda: ("Münster", "2020-01-02")
        volunteer_add.add_entry_to_table_x(
            self.c, "mysecs", "Franz Mustermann")
        self.c.execute("SELECT * FROM mysecs WHERE volunteerName = '{}'"
                       .format("Franz Mustermann"))
        volunteerName, regionName, startDate, endDate = self.c.fetchall()[0]
        volunteer_add.prompt_regionName_and_startDate = \
            container_prompt_regionName_and_startDate
        self.assertEqual(volunteerName, "Franz Mustermann")
        self.assertEqual(regionName, "Münster")
        self.assertEqual(startDate, "2020-01-02")
        self.assertEqual(endDate, "")