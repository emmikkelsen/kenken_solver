class Square():
    def __init__(self, location):
        self._location = location
        self._value: int = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    @property
    def location(self):
        return self._location
