import unittest
import os
from utils import mysec_map
from bs4 import BeautifulSoup
import databaseConnection
from _pytest.monkeypatch import MonkeyPatch


class TestMap(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMap, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/TestFilled.db"

    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.monkeypatch.setattr(
            "databaseConnection.DatabaseConnection.db_name", self.db_name)
        self.monkeypatch.setattr(
            "databaseConnection.DatabaseConnection.commit", lambda x: None)

    def tearDown(self):
        databaseConnection.DatabaseConnection.close()
        self.monkeypatch.undo()

    def test_make_looking_state_map(self):
        functionTemp = mysec_map.prompt_region_ids_for_looking_state_change
        self.monkeypatch.setattr(
            "builtins.input", lambda x: "")
        mysec_map.generate_looking_state_map(
            self.data_path, f"{self.data_path}/test_map.png")
        self.assertTrue(
            os.path.exists(f"{self.data_path}/test_map.png"),
            "test_Map.png does not exist at expected location")
        os.remove(f"{self.data_path}/test_map.png")
        mysec_map.prompt_region_ids_for_looking_state_change = functionTemp

    def test_make_mysec_presence_map(self):
        mysec_map.generate_mysec_presence_map(
            self.data_path, f"{self.data_path}/test_map.png")
        self.assertTrue(
            os.path.exists(f"{self.data_path}/test_map.png"),
            "test_Map.png does not exist at expected location")
        os.remove(f"{self.data_path}/test_map.png")

    def test_make_m_count_map(self):
        mysec_map.generate_m_count_map(
            self.data_path, f"{self.data_path}/test_map.png")
        self.assertTrue(
            os.path.exists(f"{self.data_path}/test_map.png"),
            "test_Map.png does not exist at expected location")
        os.remove(f"{self.data_path}/test_map.png")

    def test_make_my_count_map(self):
        mysec_map.generate_my_count_map(
            self.data_path, f"{self.data_path}/test_map.png")
        self.assertTrue(
            os.path.exists(f"{self.data_path}/test_map.png"),
            "test_Map.png does not exist at expected location")
        os.remove(f"{self.data_path}/test_map.png")

    def test_make_m_frequency_map(self):
        mysec_map.generate_m_frequency_map(
            self.data_path, f"{self.data_path}/test_map.png")
        self.assertTrue(
            os.path.exists(f"{self.data_path}/test_map.png"),
            "test_Map.png does not exist at expected location")
        os.remove(f"{self.data_path}/test_map.png")

    def test_make_my_frequency_map(self):
        mysec_map.generate_my_frequency_map(
            self.data_path, f"{self.data_path}/test_map.png")
        self.assertTrue(
            os.path.exists(f"{self.data_path}/test_map.png"),
            "test_Map.png does not exist at expected location")
        os.remove(f"{self.data_path}/test_map.png")

    def test_remove_malformed_attribute(self):
        soup = BeautifulSoup("""
            <?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <svg xmlns="http://www.w3.org/2000/svg">
            </svg>""", 'xml')
        mysec_map.remove_malformed_attribute_from_soup(soup)
        self.assertEqual(len(soup.svg.attrs), 0)

    def test_prompt(self):
        self.monkeypatch.setattr(
            "builtins.input", lambda x: "")
        self.assertEqual(
            mysec_map.prompt_region_ids_for_looking_state_change(), [])
        self.monkeypatch.setattr(
            "builtins.input", lambda x: "1010, 2020")
        self.assertEqual(
            mysec_map.prompt_region_ids_for_looking_state_change(),
            [1010, 2020])

    def test_get_regions_with_active_mysec(self):
        active_regions = mysec_map.get_all_regions_with_active_mysec()
        self.assertEqual(len(active_regions), 1)

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
