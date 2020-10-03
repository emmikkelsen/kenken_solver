from square import Square
from operation import Operation
from functools import reduce  # Required in Python 3
import operator
from typing import List


class Group:
    def __init__(self, members, operation, result, board):
        self._members: List[Square] = members
        self._operation: Operation = operation
        self._result: int = result
        self._permutations: List[List] = []
        self._board = board
        self._size = len(self._members)

    def _values(self):
        return [sq.value for sq in self._members]

    def locations(self):
        return [sq.location for sq in self._members]

    def prod(self, iterable):
        return reduce(operator.mul, iterable, 1)

    @property
    def members(self):
        return self._members

    @property
    def size(self):
        return self._size

    @property
    def result(self):
        return self._result

    @property
    def operation(self):
        return self._operation

    def add_permutation(self, p):
        self._permutations.append(p)

    def reset(self):
        for sq in self._members:
            sq.value = 0

    @property
    def permutations(self):
        return self._permutations

    def is_valid(self):
        if self._operation == Operation.Add:
            return sum(self._values()) == self._result
        if self._operation == Operation.Multiply:
            return self.prod(self._values()) == self._result
        if self._operation == Operation.Subtract:
            return max(self._values())-min(self._values()) == self._result
        if self._operation == Operation.Divide:
            return max(self._values())/min(self._values()) == self._result
