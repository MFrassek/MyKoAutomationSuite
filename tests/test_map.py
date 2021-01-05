import unittest
import os
from utils import mysec_map
from utils import helper
from bs4 import BeautifulSoup


class TestInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInitiation, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test.db"

    def setUp(self):
        mysec_map.Region.db_name = self.db_name
        self.conn, self.c = helper.connect_to_db(self.db_name)

    def tearDown(self):
        helper.uncommited_disconnect_from_db(self.conn)

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
        original_looking_state = mysec_map.Region.create_region_by_id("1020").looking_state
        mysec_map.toggle_looking_state_in_db("1020")
        new_looking_state = mysec_map.Region.create_region_by_id("1020").looking_state
        self.assertEqual(original_looking_state, not new_looking_state)

    def test_prompt(self):
        mysec_map.input = lambda x: ""
        self.assertEqual(
            mysec_map.prompt_region_ids_for_looking_state_change(), [])
        mysec_map.input = lambda x: "1010, 2020"
        self.assertEqual(
            mysec_map.prompt_region_ids_for_looking_state_change(),
            [1010, 2020])
        mysec_map.input = input

    def test_get_regions_details(self):
        self.assertEqual(
            len(mysec_map.get_regionIds_regionNames_and_lookingBools(self.c)),
            40)

    def test_change_fill_color(self):
        xml_path_raw = '''
        <svg>
            <path
                d="m 0,0 0,1 1,1 1,0 z"
                style="fill:#999999"
                id="Reg1" />
            <path
                d="m 2,2 c 2,1 1,1 1,2 z"
                style="fill:#999999"
                id="Reg2" />
        </svg>
        '''
        soup = BeautifulSoup(xml_path_raw, 'xml')
        mysec_map.change_fill_color_of_path(soup, "Reg1", "123456")
        self.assertEqual(soup.path["style"], "fill:#123456")
