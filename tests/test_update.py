import unittest
import os
from utils import volunteer_update_details
from utils import volunteer_add
from utils import helper


class TestInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInitiation, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test.db"

    def setUp(self):
        self.conn, self.c = helper.connect_to_db(self.db_name)

    def tearDown(self):
        volunteer_update_details.input = input
        helper.uncommited_disconnect_from_db(self.conn)

    def test_get_all_positions(self):
        all_positions = \
            volunteer_update_details.get_all_positions(self.c, "Test Name")
        self.assertEqual(all_positions, ["mysecs"])

    def test_update_volunteer_details(self):
        generator = (ele for ele in ["f", "1990-04-05"])
        volunteer_update_details.input = lambda x: next(generator)
        volunteer_update_details.update_volunteer_details(self.c, "Test Name")
        self.c.execute("""SELECT gender, birthDate FROM volunteers
                          WHERE volunteerName = 'Test Name'""")
        self.assertEqual(self.c.fetchall()[0], ("f", "1990-04-05"))

    def test_update_position_details(self):
        generator = (ele for ele in ["Kiel", "2019-03-02", "2020-03-02"])
        volunteer_update_details.input = lambda x: next(generator)
        volunteer_update_details.update_position_details(
            self.c, "Test Name", "mysecs")
        self.c.execute("""SELECT regionName, startDate, endDate FROM mysecs
                          WHERE volunteerName = 'Test Name'""")
        self.assertEqual(
            self.c.fetchall()[0], ("Kiel", "2019-03-02", "2020-03-02"))

    def test_update_value_in_table_without_input(self):
        volunteer_update_details.input = lambda x: ""
        volunteer_update_details.update_value_in_table(
            self.c, "Test Name", "mysecs", "startDate", "")
        self.c.execute("""SELECT startDate FROM mysecs
                          WHERE volunteerName = 'Test Name'""")
        self.assertEqual(self.c.fetchall()[0], ("2020-10-10",))

    def test_update_value_in_table_with_input(self):
        volunteer_update_details.input = lambda x: "2020-11-11"
        volunteer_update_details.update_value_in_table(
            self.c, "Test Name", "mysecs", "endDate", "")
        self.c.execute("""SELECT endDate FROM mysecs
                          WHERE volunteerName = 'Test Name'""")
        self.assertEqual(self.c.fetchall()[0], ("2020-11-11",))
