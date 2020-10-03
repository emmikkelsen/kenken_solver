from typing import List
from board import Board
from typing import Set, Optional
from group import Group


class Board2(Board):
    def __init__(self, size):
        super().__init__(size)
        self._row_sets: List[Set] = [set() for _ in range(size)]
        self._col_sets: List[Set] = [set() for _ in range(size)]
        self._active = []

    def try_permutation(self, i_g, i_p):
        g = self._groups[i_g]
        p = g._permutations[i_p]
        locs = g.locations()

        for loc, val in zip(locs, p):
            if val in self._row_sets[loc[0]] or val in self._col_sets[loc[1]]:
                return False
        for loc, val in zip(locs, p):
            self._row_sets[loc[0]].add(val)
            self._col_sets[loc[1]].add(val)
        self._active.append([i_g, i_p])
        return True

    def reset(self, g: Optional[Group] = None) -> None:
        if g is None:
            for sq in self._board:
                sq.value = 0
            self._active = []
            for s in self._col_sets:
                s.clear()
            for s in self._row_sets:
                s.clear()
        else:
            val = self._active.pop()
            g = self._groups[val[0]]
            p = g.permutations[val[1]]
            locs = g.locations()

            for i in range(g.size):
                self._row_sets[locs[i][0]].remove(p[i])
                self._col_sets[locs[i][1]].remove(p[i])

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
