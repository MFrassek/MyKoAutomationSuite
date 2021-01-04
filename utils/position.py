class Position():
    def __init__(
            self, title: str, region: str, held_by: str,
            start_date: str, end_date: str = "", position_id: str = None):
        self._title = title
        self._held_by = held_by
        self._region = region
        self._start_date = start_date
        self._end_date = end_date
        self._position_id = position_id
