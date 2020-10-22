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
        pass

    def test_make_png(self):
        soup = mysec_map.get_wellformed_soup_from_svg_file(self.data_path)
        mysec_map.make_png_from_soup(
            soup, "{}/test_map.png".format(self.data_path))
        self.assertTrue(
            os.path.exists("{}/test_map.png".format(self.data_path)),
            "test_Map.png does not exist at expected location")
        os.remove("{}/test_map.png".format(self.data_path))
