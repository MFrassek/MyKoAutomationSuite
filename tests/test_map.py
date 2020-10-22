import unittest
import os
from utils import mysec_map


class TestInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInitiation, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "Test.db"

    def tearDown(self):
        mysec_map.input = input

    def test_make_png(self):
        soup = mysec_map.get_wellformed_soup_from_svg_file(self.data_path)
        mysec_map.make_png_from_soup(
            soup, "{}/test_map.png".format(self.data_path))
        self.assertTrue(
            os.path.exists("{}/test_map.png".format(self.data_path)),
            "test_Map.png does not exist at expected location")
        os.remove("{}/test_map.png".format(self.data_path))

    def test_toggle(self):
        conn, c = mysec_map.connect_to_db(self.db_name)
        c.execute("SELECT looking FROM regions WHERE regionId = 1020")
        original_looking_state = c.fetchone()[0]
        mysec_map.toggle_looking_state_in_db(c, "1020")
        c.execute("SELECT looking FROM regions WHERE regionId = 1020")
        new_looking_state = c.fetchone()[0]
        self.assertEqual(not original_looking_state, new_looking_state)

    def test_prompt(self):
        mysec_map.input = lambda x: ""
        self.assertEqual(
            mysec_map.prompt_regionIds_for_looking_state_change(), [])
        mysec_map.input = lambda x: "1010, 2020"
        self.assertEqual(
            mysec_map.prompt_regionIds_for_looking_state_change(),
            [1010, 2020])
