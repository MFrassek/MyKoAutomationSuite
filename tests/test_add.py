import unittest
import os
from utils import volunteer_add


class TestInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInitiation, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "Test.db"

    def setUp(self):
        self.conn, self.c = volunteer_add.connect_to_db(self.db_name)

    def tearDown(self):
        volunteer_add.deconnect_from_db(self.conn)

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

    def test_prompt(self):
        volunteer_add.input = lambda x: ""
        self.assertEqual(
            volunteer_add.prompt_position_names(), [""])
        volunteer_add.input = lambda x: "mysecs, myvers"
        self.assertEqual(
            volunteer_add.prompt_position_names(),
            ["mysecs", "myvers"])
        volunteer_add.input = input

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
