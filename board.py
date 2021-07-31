from square import Square
from math import floor
from group import Group
from permutation import permutation
from typing import List, Optional, Sized


class Board():
    def __init__(self, size):
        self._board: List[Square] = [Square([floor(x/size), x % size])
                                     for x in range(size**2)]
        self._groups: List[Group] = []
        self._size: int = size

    def at_location(self, location):
        return next(filter(lambda x: (x.location[0] == location[0]
                                      and x.location[1] == location[1]),
                           self._board))

    def add_value(self, location, value):
        sq = next(filter(lambda x: (x.location[0] == location[0]
                                    and x.location[1] == location[1]),
                         self._board))
        sq.value = value

    def add_group(self, locations, operation, result):
        members = [self.at_location(x) for x in locations]
        self._groups.append(Group(members, operation, result, self))

    def _as_value_array(self):
        arr = [[0]*self._size for _ in range(self._size)]
        for sq in self._board:
            loc = sq.location
            arr[loc[0]][loc[1]] = sq.value
        return(arr)

    def __str__(self):
        arr = self._as_value_array()
        return arr.__str__()

    @property
    def groups(self):
        return self._groups

    def add_permutations(self):
        for g in self._groups:
            members = g.members
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
                self.reset()

        self._groups.sort(key=lambda x: len(x.permutations))

        locations = []
        for g in self._groups:
            for s in g.members:
                locations.append(s.location)
        for i in range(self._size):
            for j in range(self._size):
                assert any(list == [i, j] for list in locations)

    def reset(self, g: Optional[Group] = None) -> None:
        if g is None:
            for sq in self._board:
                sq.value = 0
        else:
            self._groups[g].reset()

    def try_permutation(self, i_g, i_p):
        g = self._groups[i_g]
        p = g._permutations[i_p]
        for i in range(len(g.members)):
            if not self.try_set(g.members[i].location, p[i]):
                for sq in g.members:
                    sq.value = 0
                return False
        return True

    def try_set(self, loc, value):
        in_row = list(filter(lambda x: x.location[0] == loc[0],
                             self._board))
        in_col = list(filter(lambda x: x.location[1] == loc[1],
                             self._board))
        s = set()
        for y in in_row:
            s.add(y.value)
        for y in in_col:
            s.add(y.value)
        if value in s:
            return False
        next(filter(lambda x: x.location[0] == loc[0]
                    and x.location[1] == loc[1],
                    self._board)).value = value
        return True

    def is_valid(self):
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
        return all([gr.is_valid() for gr in self._groups])

    @property
    def size(self):
        return self._size
