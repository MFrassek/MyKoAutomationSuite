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
        helper.uncommited_disconnect_from_db(self.conn)

    def test_get_all_positions(self):
        all_positions = \
            volunteer_update_details.get_all_positions(self.c, "Test Name")
        self.assertEqual(all_positions, ["mysecs"])

    def test_update_value_in_table_without_input(self):
        volunteer_update_details.input = lambda x: ""
        volunteer_update_details.update_value_in_table(
            self.c, "Test Name", "mysecs", "startDate", "")
        volunteer_update_details.input = input
        self.c.execute("""SELECT startDate FROM mysecs
                          WHERE volunteerName = 'Test Name'""")
        self.assertEqual(self.c.fetchall()[0], ("2020-10-10",))

    def test_update_value_in_table_with_input(self):
        volunteer_update_details.input = lambda x: "2020-11-11"
        volunteer_update_details.update_value_in_table(
            self.c, "Test Name", "mysecs", "endDate", "")
        volunteer_update_details.input = input
        self.c.execute("""SELECT endDate FROM mysecs
                          WHERE volunteerName = 'Test Name'""")
        self.assertEqual(self.c.fetchall()[0], ("2020-11-11",))
