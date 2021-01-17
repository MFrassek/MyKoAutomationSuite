import unittest
import os
from utils import region
from region import Region
from _pytest.monkeypatch import MonkeyPatch
from utils import init_db


class TestRegion(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRegion, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test.db"

    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.monkeypatch.setattr(
            "region.Region.db_name", self.db_name)
        init_db.init_db(self.data_path, self.db_name)
        Region(1020, "Kiel", "kiel", "minsh", 1).add_to_db()
        Region(1030, "Hamburg", "hamburg", "hamlet", 1).add_to_db()
        Region(1040, "Nordwest", "nordwest", "bremensie", 1).add_to_db()
        Region(2050, "Münster", "muenster", "moment", 1).add_to_db()
        Region(8005, "Aschaffenburg", "aschaffenburg", "fragment", 1)\
            .add_to_db()

    def tearDown(self):
        self.monkeypatch.undo()

    def test_region_accessibility(self):
        reg = Region(
            id_=1, name="Münster", mail_name="ms",
            magazine_name="mo", looking_state=True)
        self.assertEqual(reg.id, 1)
        self.assertEqual(reg.name, "Münster")
        self.assertEqual(reg.mail_name, "ms")
        self.assertEqual(reg.magazine_name, "mo")
        self.assertEqual(reg.looking_state, 1)

    def test_region_mutability(self):
        reg = Region(
            id_=1, name="Münster", mail_name="ms",
            magazine_name="mo", looking_state=True)
        reg.looking_state = 0
        self.assertEqual(reg.looking_state, 0)
        with self.assertRaises(AttributeError):
            reg.id = 2
        with self.assertRaises(AttributeError):
            reg.name = "New"
        with self.assertRaises(AttributeError):
            reg.mail_name = "New"
        with self.assertRaises(AttributeError):
            reg.magazine_name = "New"

    def test_region_equal(self):
        self.assertEqual(
            Region(1, "A", "B", "C", True),
            Region(1, "D", "E", "F", False))
        self.assertNotEqual(
            Region(1, "A", "B", "C", True),
            Region(2, "A", "B", "C", True))

    def test_region_hash(self):
        self.assertEqual(
            hash(Region(1, "A", "B", "C", True)),
            hash(Region(1, "D", "E", "F", False)))
        self.assertNotEqual(
            hash(Region(1, "A", "B", "C", True)),
            hash(Region(2, "A", "B", "C", True)))

    def test_region_factory_methods(self):
        self.assertEqual(len(Region.create_all()), 5)
        self.assertEqual(len(Region.create_all_fitting_data(
            [["region_id", ">", "4000"]])), 1)
        self.assertEqual(Region.create_by_name("Münster").id, 2050)
        self.assertEqual(Region.create_by_id("8005").name, "Aschaffenburg")

    def test_get_details_fitting_data(self):
        self.assertEqual(
            Region.get_details_fitting_data([["region_id", "<=", "1030"]]),
            [(1020, "Kiel", "kiel", "minsh", 1),
             (1030, "Hamburg", "hamburg", "hamlet", 1)])

    def test_update_db(self):
        reg = Region.create_by_name("Hamburg")
        original_looking_state = reg.looking_state
        reg.looking_state = int(not reg.looking_state)
        reg.update_in_db()
        reg = Region.create_by_name("Hamburg")
        new_looking_state = reg.looking_state
        self.assertNotEqual(original_looking_state, new_looking_state)
