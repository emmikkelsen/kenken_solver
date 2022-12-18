from typing import List, Set, Tuple
from .board import Board


class Board3(Board):
    """
    Representation of a KenKen board. Values in each row and column are
    represented by a set of values. E.g. if 1 is placed in square (1, 2)
    1 will be in the 1st row set and 2nd column set.
    """

    _row_sets: List[Set[int]]
    _col_sets: List[Set[int]]
    _active_groups: List[Tuple[int, int]]

    def __init__(self, size):
        super().__init__(size)
        self._row_sets = [set() for _ in range(size)]
        self._col_sets = [set() for _ in range(size)]
        self._active_groups = []

    def try_permutation(self, group_idx: int, permutation_idx: int):
        """
        Attempt to add permutation indexed by permutation_idx of group
        indexed by group_idx to board

        Return False if not possible, True if possible
        """
        group = self._groups[group_idx]
        permutation = group.permutations[permutation_idx]
        locations = group.locations()

        for location, value in zip(locations, permutation):
            # Check if choosing the permutation violates the board
            if (
                value in self._row_sets[location.x]
                or value in self._col_sets[location.y]
            ):
                return False
        for location, value in zip(locations, permutation):
            # Add the permutation
            self._row_sets[location.x].add(value)
            self._col_sets[location.y].add(value)
        self._active_groups.append((group_idx, permutation_idx))
        return True

    def remove_last_group(self) -> None:
        """
        Remove group from board
        """
        last_group_idx, last_permutation_idx = self._active_groups.pop()
        group = self._groups[last_group_idx]
        permutation = group.permutations[last_permutation_idx]
        locations = group.locations()

        for location, value in zip(locations, permutation):
            self._row_sets[location.x].remove(value)
            self._col_sets[location.y].remove(value)

    def reset_board(self) -> None:
        """
        Reset board
        """
        for sq in self._squares:
            sq.value = 0
        self._active_groups = []
        self._row_sets = [set() for _ in range(self._size)]
        self._col_sets = [set() for _ in range(self._size)]

    def is_valid(self):
        """
        Check if board is valid
        """
        for group_idx, permutation_idx in self._active_groups:
            group = self._groups[group_idx]
            permutation = group.permutations[permutation_idx]
            for location, value in zip(group.locations(), permutation):
                self.at_location(location).value = value
        return super().is_valid()

    def all_valid(self):
        """
        Check if groups are valid
        """
        for group_idx, permutation_idx in self._active_groups:
            group = self._groups[group_idx]
            permutation = group.permutations[permutation_idx]
            for location, value in zip(group.locations(), permutation):
                self.at_location(location).value = value
        return super().all_valid()
