from helper import connect_to_db, disconnect_from_db


class Region():
    db_name = "MY-Ko.db"

    def __init__(
            self, id_: int, name: str, mail_name: str, looking_state: bool):
        self._id_ = id_
        self._name = name
        self._mail_name = mail_name
        self._looking_state = looking_state

    def __repr__(self):
        return f"Region: {self._name}"

    @property
    def id_(self):
        return self._id_

    @property
    def name(self):
        return self._name

    @property
    def mail_name(self):
        return self._mail_name

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
