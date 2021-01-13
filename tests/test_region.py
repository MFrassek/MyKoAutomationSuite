import unittest
import os
from utils.region import Region


class TestInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInitiation, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test.db"

    def setUp(self):
        Region.db_name = self.db_name

    def tearDown(self):
        pass
