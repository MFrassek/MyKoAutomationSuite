import unittest
import os
from utils import init_db


class TestInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInitiation, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_weekend_file_exists(self):
        self.assertTrue(
            os.path.exists("{}/weekends.txt".format(self.data_path)),
            "weekends.txt does not exist at expected location")


if __name__ == '__main__':
    unittest.main()
