import unittest
import os
from utils import mysec_map


class TestInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInitiation, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))

    def tearDown(self):
        os.remove("{}/test_map.png".format(self.data_path))

    def test_make_png(self):
        mysec_map.generate_mysec_map(
            self.data_path,
            "{}/test_map.png".format(self.data_path),
            "Test.db")
        self.assertTrue(
            os.path.exists("{}/test_map.png".format(self.data_path)),
            "MYSec_Map.png does not exist at expected location")
