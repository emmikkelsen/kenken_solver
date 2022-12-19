from typing import NamedTuple


class Location(NamedTuple):
    """
    Representation of location as x/y coordinates on KenKen board
    """
    x: int
    y: int
