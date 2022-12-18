from .location import Location


class Square():
    """
    Representation of a square on the KenKen board
    """
    _location: Location
    _value: int
    __slots__ = ('_location', '_value')

    def __init__(self, location: Location):
        self._location = location
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    @property
    def location(self):
        return self._location
