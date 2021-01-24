from databaseEntry import DatabaseEntry
from helper import connect_to_db, disconnect_from_db


class Region(DatabaseEntry):
    table_name = "regions"

    def __init__(
            self, id_: int, name: str, mail_name: str, magazine_name: str,
            m_count: int, my_count: int, looking_state: int):
        self._id = id_
        self._name = name
        self._mail_name = mail_name
        self._magazine_name = magazine_name
        self._m_count = m_count
        self._my_count = my_count
        self._looking_state = int(looking_state)

    def __repr__(self):
        return f"Region: {self._name}"

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def mail_name(self):
        return self._mail_name

    @property
    def magazine_name(self):
        return self._magazine_name

    @property
    def m_count(self):
        return self._m_count

    @property
    def my_count(self):
        return self._my_count

    @property
    def looking_state(self):
        return self._looking_state

    @looking_state.setter
    def looking_state(self, looking_state):
        assert looking_state in [0, 1], \
            "'looking_state' must be either 0 or 1"
        self._looking_state = looking_state

    @property
    def mysec_mail_address(self):
        return f"mysec-{self._mail_name}@mensa.de"

    @classmethod
    def create_from_db_data_tuple(cls, data_tuple: tuple):
        return cls(*data_tuple)

    @classmethod
    def create_by_name(cls, name: str):
        return cls.create_all_fitting_data([["region", "=", name]])[0]

    @classmethod
    def create_by_id(cls, id_: int):
        return cls.create_all_fitting_data([["region_id", "=", str(id_)]])[0]

    def get_insertion_command(self):
        return f"""INSERT INTO regions (
                regionId, regionName, regionMailName,
                magazineName, mCount, myCount, looking)
            VALUES (
                '{self._id}', '{self._name}', '{self._mail_name}',
                '{self._magazine_name}', '{self._m_count}',
                '{self._my_count}', '{self._looking_state}');"""

    def get_update_command(self):
        return f"""UPDATE regions
            SET looking = '{self._looking_state}'
            WHERE regionName = '{self._name}';"""
