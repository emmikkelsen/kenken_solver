from typing import NamedTuple


class Location(NamedTuple):
    """
    Represntation of location as x/y coordinates on KenKen board
    """
    x: int
    y: int
