import sqlite3


class DatabaseConnection():
    db_name = "MY-Ko.db"
    _instance = None

    def __new__(cls):
        if cls._instance is not None:
            return cls._instance
        cls._instance = object.__new__(cls)
        cls._instance._init()
        return cls._instance

    def _init(self):
        self._conn = sqlite3.connect(self.__class__.db_name)
        self._c = self._conn.cursor()

    def close(self):
        self._conn.close()
        del self._c
        del self._conn
        self.__class__._instance = None

    def commit(self):
        self._conn.commit()

    def execute(self, command):
        self._c.execute(command)
