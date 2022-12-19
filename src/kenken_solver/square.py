class Square():
    """
    Representation of a square on the KenKen board
    """
    _value: int
    __slots__ = ('_value', )

    def __init__(self):
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
