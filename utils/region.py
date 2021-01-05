from helper import connect_to_db, disconnect_from_db


class Region():
    db_name = "MY-Ko.db"

    def __init__(
            self, id_: int, name: str, mail_name: str,
            magazine_name: str, looking_state: bool):
        self._id = id_
        self._name = name
        self._mail_name = mail_name
        self._magazine_name = magazine_name
        self._looking_state = looking_state

    def __repr__(self):
        return f"Region: {self._name}"

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
        assert isinstance(looking_state, bool), \
            "'looking_state' must be of type bool"
        self._looking_state = looking_state

    @staticmethod
    def create_region(name: str):
        conn, c = connect_to_db(Region.db_name)
        c.execute(
            f"""SELECT *
            FROM regions
            WHERE regionName = '{name}'""")
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
