import unittest
import os
from utils import volunteer_add
from utils import init_db
from _pytest.monkeypatch import MonkeyPatch


class TestInitiation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInitiation, self).__init__(*args, **kwargs)
        self.data_path = "{}/test_data".format(
            os.path.dirname(os.path.abspath(__file__)))
        self.db_name = "tests/Test_add.db"

    def setUp(self):
        volunteer_add.Position.db_name = self.db_name
        volunteer_add.Volunteer.db_name = self.db_name
        init_db.init_db(self.data_path, self.db_name)
        self.monkeypatch = MonkeyPatch()

    def tearDown(self):
        self.monkeypatch.undo()

    def test_add_volunteer(self):
        generator = (ele for ele in ["1995-03-03", "d"])
        self.monkeypatch.setattr("builtins.input", lambda x: next(generator))
        volunteer_add.add_new_volunteer("Test Person")
        self.assertEqual(len(volunteer_add.Volunteer.create_all()), 1)

    def test_add_entry_to_mysecs(self):
        container_prompt_regionName_and_startDate = \
            volunteer_add.prompt_regionName_and_startDate
        volunteer_add.prompt_regionName_and_startDate = \
            lambda: ("Münster", "2020-01-02")
        volunteer_add.add_entry_to_table_x(
            self.c, "mysecs", "Franz Mustermann")
        self.c.execute("SELECT * FROM mysecs WHERE volunteerName = '{}'"
                       .format("Franz Mustermann"))
        volunteerName, regionName, startDate, endDate = self.c.fetchall()[0]
        volunteer_add.prompt_regionName_and_startDate = \
            container_prompt_regionName_and_startDate
        self.assertEqual(volunteerName, "Franz Mustermann")
        self.assertEqual(regionName, "Münster")
        self.assertEqual(startDate, "2020-01-02")
        self.assertEqual(endDate, "")