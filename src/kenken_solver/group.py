from .location import Location
from .operation import Operation
from functools import reduce  # Required in Python 3
import operator
from typing import MutableSequence, Sequence


class Group:
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

    def prod(self, iterable):
        return reduce(operator.mul, iterable, 1)

    @property
    def locations(self):
        return self._locations

    @property
    def size(self):
        return self._size

    @property
    def result(self):
        return self._result

    @property
    def operation(self):
        return self._operation

    def add_permutations(self):
        permutations = self.all_permutations()
        x_values = [loc.x for loc in self._locations]
        y_values = [loc.y for loc in self._locations]

        for permutation in permutations:
            if (
                len(set(zip(permutation, x_values)))
                == len(set(zip(permutation, y_values)))
                == self._size
            ):
                self._permutations.append(permutation)

    def reset(self):
        for sq in self._locations:
            sq.value = 0

    @property
    def permutations(self):
        return self._permutations

    def permutation_is_valid(self, permutation: Sequence[int]):
        if self._operation == Operation.Add:
            return sum(permutation) == self._result
        if self._operation == Operation.Multiply:
            return self.prod(permutation) == self._result
        if self._operation == Operation.Subtract:
            return max(permutation)-min(permutation) == self._result
        if self._operation == Operation.Divide:
            return max(permutation)/min(permutation) == self._result

    def all_permutations(self) -> Sequence[Sequence[int]]:
        """
        Generate all com
        """

        if self._operation == Operation.Divide:
            maxes = list(filter(lambda x: x % self._result == 0 and x > 0,
                                range(self._max_value+1)))
            mins = [m//self._result for m in maxes]
            p = []
            for x in range(len(maxes)):
                p.append([maxes[x], mins[x]])
                p.append([mins[x], maxes[x]])
            return p

        if self._operation == Operation.Subtract:
            maxes = list(
                filter(lambda x: x > self._result, range(self._max_value+1))
            )
            mins = [m - self._result for m in maxes]
            p = []
            for x in range(len(maxes)):
                p.append([maxes[x], mins[x]])
                p.append([mins[x], maxes[x]])
            return p

        if self._operation == Operation.Add:
            return _permutations_add(self._max_value, self._result, self._size)

        if self._operation == Operation.Multiply:
            return _permutations_multiply(self._max_value, self._result,
                                          self._size)


def _permutations_add(ma, res, n):
    if n == 1:
        return [[res]]
    t = []
    for x in range(1, ma+1):
        if (res-x)/(n-1) <= ma and res-x >= n-1:
            for ss in _permutations_add(ma, res-x, n-1):
                t.append(ss + [x])
    return t


def _permutations_multiply(ma, res, n):
    if n == 1:
        return [[res]]
    t = []
    factors = list(filter(lambda x: res % x == 0, range(1, ma+1)))
    for x in factors:
        if res//x <= ma**(n-1):
            for ss in _permutations_multiply(ma, res//x, n-1):
                t.append(ss + [int(x)])
    return t
