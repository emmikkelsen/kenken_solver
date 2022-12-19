from .location import Location
from .operation import Operation
from .square import Square
from math import floor
from .group import Group
from ...unused.permutation import permutation
from typing import List, Optional, Sequence


class Board():
    """
    Representation of KenKen board
    """

    _groups: Sequence[Group]
    _size: int
    _squares: Sequence[Square]

    def __init__(self, size):
        # Create all squares on board
        self._squares = [Square(Location(floor(x/size), x % size))
                         for x in range(size**2)]
        self._groups = []
        self._size = size

    def at_location(self, location: Location):
        """
        Get square at location
        """
        return next(
            filter(
                lambda square: (square.location.x == location.x
                                and square.location.y == location.y),
                self._squares
            )
        )

    def set_value_of_square(self, location: Location, value: int):
        """
        Set value of square at location
        """
        sq = self.at_location(location)
        sq.value = value

    def add_group_to_board(
        self,
        locations: Sequence[List[int]],
        operation: Operation,
        result: int
    ):
        """
        Add group to board
        """
        members = [self.at_location(Location(x[0], x[1])) for x in locations]
        self._groups.append(Group(members, operation, result, self))

    @property
    def groups(self):
        return self._groups

    def add_permutations(self):
        """
        Add permutations to groups on board
        """
        for g in self._groups:
            members = g.locations
            n = len(members)
            permutations = permutation(self._size,
                                       n,
                                       g.operation,
                                       g.result)
            for p in permutations:
                for i in range(n):
                    members[i].value = p[i]
                if self.is_valid():
                    g.add_permutation(p)
                self.reset_board()

        self._groups.sort(key=lambda x: len(x.permutations))

        locations = []
        for g in self._groups:
            for s in g.locations:
                locations.append(s.location)
        for i in range(self._size):
            for j in range(self._size):
                assert any(location == Location(i, j) for location in locations)

    def remove_group(self, g: int) -> None:
        self._groups[g].reset()

    def reset_board(self) -> None:
        for sq in self._squares:
            sq.value = 0

    def try_permutation(self, i_g, i_p):
        g = self._groups[i_g]
        p = g._permutations[i_p]
        for i in range(len(g.locations)):
            if not self.try_set(g.locations[i].location, p[i]):
                for sq in g.locations:
                    sq.value = 0
                return False
        return True

    def try_set(self, loc, value):
        in_row = list(filter(lambda x: x.location[0] == loc[0],
                             self._squares))
        in_col = list(filter(lambda x: x.location[1] == loc[1],
                             self._squares))
        s = set()
        for y in in_row:
            s.add(y.value)
        for y in in_col:
            s.add(y.value)
        if value in s:
            return False
        next(filter(lambda x: x.location[0] == loc[0]
                    and x.location[1] == loc[1],
                    self._squares)).value = value
        return True

    def is_valid(self):
        """
        Check if board is valid
        """
        arr = self._as_value_array()
        for x in range(self._size):
            row = arr[x]
            s = set()
            for y in row:
                if y in s:
                    return False
                if y > 0:
                    s.add(y)
        for x in range(self._size):
            col = [arr[y][x] for y in range(self._size)]
            s = set()
            for y in col:
                if y in s:
                    return False
                if y > 0:
                    s.add(y)
        return True

    def all_valid(self):
        """
        Check if all groups are valid
        """
        return all([gr.is_valid() for gr in self._groups])

    @property
    def size(self):
        return self._size

    def _as_value_array(self):
        """
        Represent board as array of integer values
        """
        arr = [[0]*self._size for _ in range(self._size)]
        for sq in self._squares:
            loc = sq.location
            arr[loc[0]][loc[1]] = sq.value
        return arr

    def __str__(self):
        return str(self._as_value_array())
