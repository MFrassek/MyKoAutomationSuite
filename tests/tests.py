import unittest
import os
from utils import init_db


class TestInitiation(unittest.TestCase):
    def setUp(self):
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))

    def tearDown(self):
        pass




if __name__ == '__main__':
    unittest.main()
