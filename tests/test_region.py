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

    def test_region_accessibility(self):
        reg = Region(
            id_=1, name="Münster", mail_name="ms",
            magazine_name="mo", looking_state=True)
        self.assertEqual(reg.id, 1)
        self.assertEqual(reg.name, "Münster")
        self.assertEqual(reg.mail_name, "ms")
        self.assertEqual(reg.magazine_name, "mo")
        self.assertEqual(reg.looking_state, 1)
