import unittest
from utils.region import Region
import databaseConnection
from _pytest.monkeypatch import MonkeyPatch


class TestRegion(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRegion, self).__init__(*args, **kwargs)
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

    def test_region_accessibility(self):
        reg = Region(
            id_=1, name="Münster", mail_name="ms",
            magazine_name="mo", m_count=5, my_count=3, non_m_count=10,
            looking_state=True)
        self.assertEqual(reg.id, 1)
        self.assertEqual(reg.name, "Münster")
        self.assertEqual(reg.mail_name, "ms")
        self.assertEqual(reg.magazine_name, "mo")
        self.assertEqual(reg.m_count, 5)
        self.assertEqual(reg.my_count, 3)
        self.assertEqual(reg.non_m_count, 10)
        self.assertEqual(reg.looking_state, 1)

    def test_region_mutability(self):
        reg = Region(
            id_=1, name="Münster", mail_name="ms",
            magazine_name="mo", m_count=5, my_count=3, non_m_count=10,
            looking_state=True)
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
        with self.assertRaises(AttributeError):
            reg.m_count = 7
        with self.assertRaises(AttributeError):
            reg.my_count = 1
        with self.assertRaises(AttributeError):
            reg.non_m_count = 2

    def test_region_equal(self):
        self.assertEqual(
            Region(1, "A", "B", "C", 1, 1, 1, True),
            Region(1, "D", "E", "F", 2, 3, 4, False))
        self.assertNotEqual(
            Region(1, "A", "B", "C", 1, 1, 1, True),
            Region(2, "A", "B", "C", 1, 1, 1, True))

    def test_region_hash(self):
        self.assertEqual(
            hash(Region(1, "A", "B", "C", 1, 1, 1, True)),
            hash(Region(1, "D", "E", "F", 2, 3, 4, False)))
        self.assertNotEqual(
            hash(Region(1, "A", "B", "C", 1, 1, 1, True)),
            hash(Region(2, "A", "B", "C", 1, 1, 1, True)))

    def test_region_factory_methods(self):
        self.assertEqual(len(Region.create_all()), 5)
        self.assertEqual(len(Region.create_all_fitting_data(
            [["region_id", ">", "4000"]])), 1)
        self.assertEqual(Region.create_by_name("Münster").id, 2050)
        self.assertEqual(Region.create_by_id("8005").name, "Aschaffenburg")

    def test_get_details_fitting_data(self):
        self.assertEqual(
            Region.get_details_fitting_data([["region_id", "<=", "1030"]]),
            [(1020, "Kiel", "kiel", "minsh", 3, 1, 5, 1),
             (1030, "Hamburg", "hamburg", "hamlet", 5, 2, 10, 1)])

    def test_update_db(self):
        reg = Region.create_by_name("Hamburg")
        original_looking_state = reg.looking_state
        reg.looking_state = int(not reg.looking_state)
        reg.update_in_db()
        reg = Region.create_by_name("Hamburg")
        new_looking_state = reg.looking_state
        self.assertNotEqual(original_looking_state, new_looking_state)
