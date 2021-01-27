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

    @classmethod
    def close(cls):
        if cls._instance is not None:
            cls._instance.commit()
            cls._instance._conn.close()
            del cls._instance._c
            del cls._instance._conn
            cls._instance = None

    def commit(self):
        print("AAAA")
        self._conn.commit()

    def change(self, command):
        self._c.execute(command)

    def query(self, command):
        self._c.execute(command)
        return self._c.fetchall()
