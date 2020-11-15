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
        generator = (ele for ele in
                     ["Test Name", "d", "1990-10-21",
                      "mysecs", "Münster", "2020-10-10"])
        volunteer_add.input = lambda x: next(generator)
        volunteer_add.add_new_volunteer_and_position(self.db_name)
        volunteer_add.input = input
        all_positions = \
            volunteer_update_details.get_all_positions(self.c, "Test Name")
        self.assertEqual(all_positions, ["mysecs"])
