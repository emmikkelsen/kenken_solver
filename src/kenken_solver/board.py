from math import floor
from typing import List, Mapping, NamedTuple, Sequence, Set, Union

from .group import Group
from .location import Location
from .operation import Operation
from .square import Square


class GroupPermutation(NamedTuple):
    """
    Group and permuation collection
    """
    group_idx: int
    permutation_idx: int


class Board():
    """
    Representation of a KenKen board. Values in each row and column are
    represented by a set of values. E.g. if 1 is placed in square (1, 2)
    1 will be in the 1st row set and 2nd column set.
    """
    _groups: Sequence[Group]
    _size: int
    _squares: Mapping[Location, Square]
    _row_sets: List[Set[int]]
    _col_sets: List[Set[int]]
    _active_groups: List[GroupPermutation]

    _iterations: int  # Amount of permutations tried by solver

    def __init__(self, size):
        self._squares = {
            Location(floor(x/size), x % size): Square()
            for x in range(size**2)
        }
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
        locations = group.locations

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
        locations = group.locations

        for location, value in zip(locations, permutation):
            self._row_sets[location.x].remove(value)
            self._col_sets[location.y].remove(value)

        return GroupPermutation(last_group_idx, last_permutation_idx)

    def reset_board(self) -> None:
        """
        Reset board
        """
        for _, square in self._squares.items():
            square.value = 0
        self._active_groups = []
        self._row_sets = [set() for _ in range(self._size)]
        self._col_sets = [set() for _ in range(self._size)]

    def _as_value_array(self):
        """
        Helper function to set square values and print board
        """
        for group_idx, permutation_idx in self._active_groups:
            group = self._groups[group_idx]
            permutation = group.permutations[permutation_idx]
            for location, value in zip(group.locations, permutation):
                self.at_location(location).value = value

        arr = [[0]*self._size for _ in range(self._size)]
        for location, square in self._squares.items():
            arr[location.x][location.y] = square.value
        return arr

    def solve_recursive(self):
        """
        Solve board recursively
        """
        self._iterations = 0

        def t(group_idx: int, permutation_idx: int) -> Union[List[int], bool]:
            """
            Recursion function. When a valid permutation is found and added,
            tries to find valid permutation in next group until last
            group is reached and valid permutation is found.

            If no valid permutation is found for a group, then steps to next
            permutation in prior group
            """
            self._iterations += 1

            if self.try_permutation(group_idx, permutation_idx):
                # Permutation p of group g is valid
                if group_idx == len(self._groups) - 1:
                    # Solution found, since permutation
                    # of last group has been assigned
                    return [(group_idx, permutation_idx)]

                next_group = t(group_idx+1, 0)  # Try next group
                if next_group:
                    next_group.append([group_idx, permutation_idx])
                    return next_group
                if group_idx == 0:
                    raise Exception('No valid solutions found')
                self.remove_last_group()
            if permutation_idx == len(self._groups[group_idx].permutations)-1:
                # Return False if no permutations found for group
                return False
            return t(group_idx, permutation_idx+1)
        return t(0, 0)

    def solve(self):
        """
        Solve board using loop. Uses same logic as recursive solver
        """
        self._iterations = 0

        solved = False
        cgp = GroupPermutation(0, 0)
        while not solved:
            self._iterations += 1
            if cgp.group_idx == len(self._groups):
                solved = True
            elif (
                len(self._groups[cgp.group_idx].permutations)
                == cgp.permutation_idx
            ):
                # Step down, since no valid permutation is available
                if cgp.group_idx == 0:
                    raise Exception('No valid solutions found')
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
    def iterations(self):
        return self._iterations

    def add_group_to_board(
        self,
        locations: Sequence[Location],
        operation: Operation,
        result: int
    ):
        """
        Add group to board
        """
        self._groups.append(Group(locations, operation, result, self._size))

    def at_location(self, location: Location):
        """
        Get square at location
        """
        return self._squares[location]

    def add_permutations(self):
        """
        Add permutations to groups on board
        """
        for group in self._groups:
            group.add_permutations()

        # Sort groups by amount of permutations for fast solving
        self._groups.sort(key=lambda x: len(x.permutations))

        # Consistency check. Check all locations covered by groups
        locations = [loc for group in self._groups for loc in group.locations]
        for i in range(self._size):
            for j in range(self._size):
                if Location(i, j) not in locations:
                    raise Exception(
                        f'{Location(i, j)} not found on board'
                    )

    def board_is_valid(self):
        """
        Check if board is valid
        """
        arr = self._as_value_array()
        for i in range(self._size):
            row = set(arr[i])
            if not all(x + 1 in row for x in range(self._size)):
                return False
        for i in range(self._size):
            col = set(arr[y][i] for y in range(self._size))
            if not all(x + 1 in col for x in range(self._size)):
                return False
        return True

    def all_groups_valid(self):
        """
        Check if all groups are valid
        """
        return all(
            gr.permutation_is_valid(
                [self._squares[loc].value for loc in gr.locations]
            ) for gr in self._groups
        )

    def __str__(self):
        return '\n'.join(str(row) for row in self._as_value_array())
