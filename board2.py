from typing import List
from board import Board
from typing import Set, Optional
from group import Group


class Board2(Board):
    def __init__(self, size):
        super().__init__(size)
        self._row_sets: List[List[bool]] = \
            [[False for _ in range(size)] for _ in range(size)]
        self._col_sets: List[List[bool]] = \
            [[False for _ in range(size)] for _ in range(size)]
        self._active = []

    def try_permutation(self, i_g, i_p):
        g = self._groups[i_g]
        p = g._permutations[i_p]
        locs = g.locations()

        for loc, val in zip(locs, p):
            if self._row_sets[loc[0]][val-1] or self._col_sets[loc[1]][val-1]:
                return False
        for loc, val in zip(locs, p):
            self._row_sets[loc[0]][val-1] = True
            self._col_sets[loc[1]][val-1] = True
        self._active.append([i_g, i_p])
        return True

    def reset(self, g: Optional[Group] = None) -> None:
        if g is None:
            for sq in self._board:
                sq.value = 0
            self._active = []
            self._row_sets = [[False for _ in range(self._size)]
                              for _ in range(self._size)]
            self._col_sets = [[False for _ in range(self._size)]
                              for _ in range(self._size)]
        else:
            v = self._active.pop()
            g = self._groups[v[0]]
            p = g.permutations[v[1]]
            locs = g.locations()

            for loc, val in zip(locs, p):
                self._row_sets[loc[0]][val-1] = False
                self._col_sets[loc[1]][val-1] = False

    def is_valid(self):
        #super().reset()
        for x in self._active:
            g = self._groups[x[0]]
            p = g.permutations[x[1]]
            for loc, val in zip(g.locations(), p):
                next(filter(lambda x: x.location[0] == loc[0]
                     and x.location[1] == loc[1],
                     self._board)).value = val
        return super().is_valid()

    def all_valid(self):
        #super().reset()
        for x in self._active:
            g = self._groups[x[0]]
            p = g.permutations[x[1]]
            for loc, val in zip(g.locations(), p):
                next(filter(lambda x: x.location[0] == loc[0]
                     and x.location[1] == loc[1],
                     self._board)).value = val
        return super().all_valid()
