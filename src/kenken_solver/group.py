import operator
from functools import reduce
from typing import MutableSequence, Sequence

from .location import Location
from .operation import Operation


class Group:
    """
    Representation of group on KenKen board
    """
    _locations: Sequence[Location]
    _operation: Operation
    _result: int
    _permutations: MutableSequence[Sequence[int]]
    _max_value: int
    _size: int

    def __init__(
        self,
        locations: Sequence[Location],
        operation: Operation,
        result: int,
        max_value: int
    ):
        self._locations = locations
        self._operation = operation
        self._result = result
        self._max_value = max_value
        self._size = len(self._locations)
        self._permutations = []

    @property
    def locations(self):
        """
        Group locations
        """
        return self._locations

    @property
    def size(self):
        """
        Group size
        """
        return self._size

    @property
    def result(self):
        """
        Group result
        """
        return self._result

    @property
    def operation(self):
        """
        Group operation
        """
        return self._operation

    @property
    def permutations(self):
        """
        Group permutations
        """
        return self._permutations

    def add_permutations(self):
        """
        Set permutations for group
        """
        permutations = self.all_permutations()
        x_values = [loc.x for loc in self._locations]
        y_values = [loc.y for loc in self._locations]

        for permutation in permutations:
            # Check whether permutation includes duplicates
            # in same row or column before adding
            if (
                len(set(zip(permutation, x_values)))
                == len(set(zip(permutation, y_values)))
                == self._size
            ):
                self._permutations.append(permutation)

    def permutation_is_valid(self, permutation: Sequence[int]):
        """
        Check if permutation is valid for group
        """
        if self._operation == Operation.ADD:
            return sum(permutation) == self._result
        if self._operation == Operation.MULTIPLY:
            return _prod(permutation) == self._result
        if self._operation == Operation.SUBTRACT:
            return max(permutation)-min(permutation) == self._result
        if self._operation == Operation.DIVIDE:
            return max(permutation)/min(permutation) == self._result
        raise Exception('Operation is not valid')

    def all_permutations(self) -> Sequence[Sequence[int]]:
        """
        Generate all possible permutations for group
        """
        if self._operation == Operation.DIVIDE:
            maxes = list(filter(lambda x: x % self._result == 0 and x > 0,
                                range(self._max_value+1)))
            mins = [m//self._result for m in maxes]
            permutations = []
            for i in range(len(maxes)):
                permutations.append([maxes[i], mins[i]])
                permutations.append([mins[i], maxes[i]])
            return permutations

        if self._operation == Operation.SUBTRACT:
            maxes = list(
                filter(lambda x: x > self._result, range(self._max_value+1))
            )
            mins = [m - self._result for m in maxes]
            permutations = []
            for i in range(len(maxes)):
                permutations.append([maxes[i], mins[i]])
                permutations.append([mins[i], maxes[i]])
            return permutations

        if self._operation == Operation.ADD:
            return _permutations_add(self._max_value, self._result, self._size)

        if self._operation == Operation.MULTIPLY:
            return _permutations_multiply(self._max_value, self._result,
                                          self._size)

        raise Exception('Invalid operation for group')


def _permutations_add(max_value: int, result: int, amount: int):
    """
    Generate all permutations by addition
    """
    if amount == 1:
        return [[result]]
    solutions = []
    for i in range(1, max_value+1):
        if (result-i)/(amount-1) <= max_value and result-i >= amount-1:
            for solution in _permutations_add(max_value, result-i, amount-1):
                solutions.append(solution + [i])
    return solutions


def _permutations_multiply(max_value: int, result: int, amount: int):
    """
    Generate all permutations by multiplication
    """
    if amount == 1:
        return [[result]]
    t = []
    factors = list(filter(lambda x: result % x == 0, range(1, max_value+1)))
    for x in factors:
        if result//x <= max_value**(amount-1):
            for solution in _permutations_multiply(
                    max_value, result//x, amount-1):
                t.append(solution + [int(x)])
    return t


def _prod(iterable):
    """
    Helper function for multiplication
    """
    return reduce(operator.mul, iterable, 1)
