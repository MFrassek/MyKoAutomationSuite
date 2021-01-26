from databaseEntry import DatabaseEntry


class WeekendParticipation(DatabaseEntry):
    table_name = "weekend_participant"

    def __init__(self, weekend_id: int, participant_name: str):
        self._weekend_id = weekend_id
        self._participant_name = participant_name

    def __repr__(self):
        return f"Participation by {self._participant_name} " \
            + f"at weekend {self._weekend_id}"

    def __hash__(self):
        return hash(self._weekend_id) ^ hash(self._participant_name)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.weekend_id == other.weekend_id \
                and self.participant_name == other.participant_name
        else:
            return False

    @property
    def weekend_id(self):
        return self._weekend_id

    @property
    def participant_name(self):
        return self._participant_name

    @classmethod
    def create_from_db_data_tuple(cls, data_tuple: tuple):
        return cls(*data_tuple)

    @classmethod
    def create_by_participant_name(cls, name: str):
        return cls.create_all_fitting_data([["name", "=", name]])[0]

    @classmethod
    def create_by_weekend_id(cls, id_: int):
        return cls.create_all_fitting_data([["weekend_id", "=", str(id_)]])[0]

    def get_insertion_command(self):
        return f"""INSERT INTO weekend_participant (
                weekendId, personName)
            VALUES (
                '{self._weekend_id}', '{self._participant_name}');"""
