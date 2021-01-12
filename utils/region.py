from databaseEntry import DatabaseEntry
from helper import connect_to_db, disconnect_from_db


class Region(DatabaseEntry):
    def __init__(
            self, id_: int, name: str, mail_name: str,
            magazine_name: str, looking_state: int):
        self._id = id_
        self._name = name
        self._mail_name = mail_name
        self._magazine_name = magazine_name
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
    def looking_state(self):
        return self._looking_state

    @looking_state.setter
    def looking_state(self, looking_state):
        assert looking_state in [0, 1], \
            "'looking_state' must be either 0 or 1"
        self._looking_state = looking_state

    @classmethod
    def create_entry_from_db_data_tuple(cls, data_tuple: tuple):
        return cls(*data_tuple)

    @classmethod
    def get_entry_details_fitting_data(cls, c, commands: list):
        assert len(commands) > 0, \
            "At least one specifying command must be given"
        c.execute(
            """SELECT *
            FROM regions
            WHERE """
            + " AND ".join(
             [cls.argument_name_to_column_name(command[0])
              + f" {command[1]} '{' '.join(command[2:])}'"
              for command in commands]))
        return c.fetchall()

    @classmethod
    def create_region_by_name(cls, name: str):
        return cls.create_all_entries_fitting_data([["region", "=", name]])[0]

    @classmethod
    def create_region_by_id(cls, id_: str):
        return cls.create_all_entries_fitting_data([["region_id", "=", id_]])[0]

    @classmethod
    def create_all_regions(cls):
        return cls.create_all_entries_fitting_data([["", "=", ""]])

    def update_in_db(self):
        conn, c = connect_to_db(DatabaseEntry.db_name)
        c.execute(f"""UPDATE regions
            SET looking = '{self._looking_state}'
            WHERE regionName = '{self._name}';""")
        disconnect_from_db(conn)
