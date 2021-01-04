class Region():
    def __init__(self, id_: int, name: str, mail_name: str, looking_state: bool)
    self._id_ = id_
    self._name = name
    self._mail_name = mail_name
    self._looking_state = looking_state

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
