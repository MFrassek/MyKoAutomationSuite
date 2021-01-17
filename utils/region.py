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

    @property
    def mysec_mail_address(self):
        return f"mysec-{self._mail_name}@mensa.de"


    @classmethod
    def create_from_db_data_tuple(cls, data_tuple: tuple):
        return cls(*data_tuple)

    @classmethod
    def get_details_fitting_data(cls, commands: list):
        assert len(commands) > 0, \
            "At least one specifying command must be given"
        conn, c = connect_to_db(cls.db_name)
        c.execute(
            """SELECT *
            FROM regions
            WHERE """
            + " AND ".join(
             [cls.argument_name_to_column_name(command[0])
              + f" {command[1]} '{' '.join(command[2:])}'"
              for command in commands]))
        result = c.fetchall()
        disconnect_from_db(conn)
        return result

    @classmethod
    def create_by_name(cls, name: str):
        return cls.create_all_fitting_data([["region", "=", name]])[0]

    @classmethod
    def create_by_id(cls, id_: str):
        return cls.create_all_fitting_data([["region_id", "=", id_]])[0]

    def update_in_db(self):
        conn, c = connect_to_db(self.__class__.db_name)
        c.execute(f"""UPDATE regions
            SET looking = '{self._looking_state}'
            WHERE regionName = '{self._name}';""")
        disconnect_from_db(conn)

    def get_insertion_command(self):
        return f"""INSERT INTO regions (
                regionId, regionName, regionMailName, magazineName, looking)
            VALUES (
                '{self._id}', '{self._name}', '{self._mail_name}',
                '{self._magazine_name}', '{self._looking_state}');"""
