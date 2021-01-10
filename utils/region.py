from helper import connect_to_db, disconnect_from_db


class Region():
    db_name = "MY-Ko.db"

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

    @staticmethod
    def create_region_by_name(name: str):
        conn, c = connect_to_db(Region.db_name)
        c.execute(
            f"""SELECT *
            FROM regions
            WHERE regionName = '{name}'""")
        data_tuple = c.fetchall()[0]
        disconnect_from_db(conn)
        return Region(*data_tuple)

    @staticmethod
    def create_region_by_id(id_: str):
        conn, c = connect_to_db(Region.db_name)
        c.execute(
            f"""SELECT *
            FROM regions
            WHERE regionId = '{id_}'""")
        data_tuple = c.fetchall()[0]
        disconnect_from_db(conn)
        return Region(*data_tuple)

    @staticmethod
    def create_all_regions():
        conn, c = connect_to_db(Region.db_name)
        c.execute("SELECT * FROM regions")
        regions = [Region(*data_tuple) for data_tuple in c.fetchall()]
        disconnect_from_db(conn)
        return regions

    def update_in_db(self):
        conn, c = connect_to_db(Region.db_name)
        c.execute(f"""UPDATE regions
            SET looking = '{self._looking_state}'
            WHERE regionName = '{self._name}';""")
        disconnect_from_db(conn)