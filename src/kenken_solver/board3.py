from math import floor
from typing import List, NamedTuple, Sequence, Set, Union

from .permutation import permutation
from .operation import Operation
from .location import Location
from .square import Square
from .group import Group


class GroupPermutation(NamedTuple):
    group_idx: int
    permutation_idx: int


class Board3():
    """
    Representation of a KenKen board. Values in each row and column are
    represented by a set of values. E.g. if 1 is placed in square (1, 2)
    1 will be in the 1st row set and 2nd column set.
    """

    _groups: Sequence[Group]
    _size: int
    _squares: Sequence[Square]
    _row_sets: List[Set[int]]
    _col_sets: List[Set[int]]
    _active_groups: List[GroupPermutation]

    _permuations_tried: int  # Amount of permutations tried by solver

    def __init__(self, size):
        self._squares = [Square(Location(floor(x/size), x % size))
                         for x in range(size**2)]
        self._groups = []
        self._size = size
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
        self._active_groups.append(
            GroupPermutation(group_idx, permutation_idx))
        return True

    def remove_last_group(self) -> GroupPermutation:
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

        return GroupPermutation(last_group_idx, last_permutation_idx)

    def reset_board(self) -> None:
        """
        Reset board
        """
        for sq in self._squares:
            sq.value = 0
        self._active_groups = []
        self._row_sets = [set() for _ in range(self._size)]
        self._col_sets = [set() for _ in range(self._size)]

    def _as_value_array(self):
        for group_idx, permutation_idx in self._active_groups:
            group = self._groups[group_idx]
            permutation = group.permutations[permutation_idx]
            for location, value in zip(group.locations(), permutation):
                self.at_location(location).value = value

        arr = [[0]*self._size for _ in range(self._size)]
        for sq in self._squares:
            loc = sq.location
            arr[loc.x][loc.y] = sq.value
        return arr

    def solve_recursive(self):
        self._permuations_tried = 0

        def t(g: int, p: int) -> Union[List[int], bool]:
            """
            Helper function for recursion
            """
            self._permuations_tried += 1

            if self.try_permutation(g, p):
                # Permutation p of group g is valid
                if g == len(self._groups) - 1:
                    # Solution found, since permutation
                    # of last group has been assigned
                    return [(g, p)]

                next_group = t(g+1, 0)  # Try next group
                if next_group:
                    next_group.append([g, p])
                    return next_group
                else:
                    self.remove_last_group()
            if p == len(self._groups[g].permutations) - 1:
                # Return False if no permutations found for group
                return False
            return t(g, p+1)

        return t(0, 0)

    def solve(self):
        self._permuations_tried = 0

        solved = False
        cgp = GroupPermutation(0, 0)
        while not solved:
            self._permuations_tried += 1
            if cgp.group_idx == len(self._groups):
                solved = True
            elif (
                len(self._groups[cgp.group_idx].permutations)
                == cgp.permutation_idx
            ):
                # Step down, since no valid permutation is available
                last_group = self.remove_last_group()
                cgp = GroupPermutation(
                    last_group.group_idx,
                    last_group.permutation_idx + 1
                )
            elif self.try_permutation(*cgp):
                # Step up one group if permutation is valid
                cgp = GroupPermutation(cgp.group_idx + 1, 0)
            else:
                # Check next permutation
                cgp = GroupPermutation(cgp.group_idx, cgp.permutation_idx + 1)
        return self._active_groups

    @property
    def permutations_tried(self):
        return self._permuations_tried

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

    def add_permutations(self):
        """
        Add permutations to groups on board
        """
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
                self.reset_board()

        self._groups.sort(key=lambda x: len(x.permutations))

        locations = []
        for g in self._groups:
            for s in g.members:
                locations.append(s.location)
        for i in range(self._size):
            for j in range(self._size):
                assert any(location == Location(i, j) for location in locations)

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

    def __str__(self):
        return str(self._as_value_array())
