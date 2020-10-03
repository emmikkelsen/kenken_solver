from typing import List, Union
from board import Board
from board2 import Board2
from operation import Operation

"""
N = 4
board = Board(N)

board.add_group([[0, 0], [1, 0], [0, 1]], Operation.Multiply, 12)
board.add_group([[1, 1], [1, 2]], Operation.Subtract, 1)
board.add_group([[0, 2], [0, 3]], Operation.Divide, 2)
board.add_group([[1, 3], [2, 3]], Operation.Subtract, 3)
board.add_group([[2, 0], [2, 1]], Operation.Subtract, 1)
board.add_group([[3, 0], [3, 1]], Operation.Divide, 2)
board.add_group([[2, 2], [3, 2], [3, 3]], Operation.Add, 7)

board.add_permutations()
"""

N = 7
board = Board2(N)

board.add_group([[0, 0], [1, 0], [1, 1]], Operation.Add, 14)
board.add_group([[0, 1], [0, 2], [1, 2]], Operation.Add, 11)
board.add_group([[0, 3], [0, 4]], Operation.Add, 3)
board.add_group([[0, 5]], Operation.Add, 5)
board.add_group([[1, 3], [1, 4], [1, 5]], Operation.Add, 18)
board.add_group([[0, 6], [1, 6], [2, 6]], Operation.Add, 11)

board.add_group([[2, 0], [3, 0], [4, 0], [2, 1], [2, 2]], Operation.Add, 12)
board.add_group([[2, 3], [3, 3]], Operation.Add, 9)
board.add_group([[2, 4], [2, 5], [3, 4]], Operation.Add, 17)
board.add_group([[3, 1], [3, 2], [4, 1]], Operation.Add, 12)
board.add_group([[3, 5], [3, 6]], Operation.Add, 3)


board.add_group([[4, 2], [4, 3], [4, 4]], Operation.Add, 13)
board.add_group([[4, 5], [4, 6], [5, 6]], Operation.Add, 19)
board.add_group([[5, 0], [6, 0], [5, 1], [6, 1]], Operation.Add, 19)
board.add_group([[5, 2], [6, 2], [5, 3]], Operation.Add, 13)
board.add_group([[6, 3], [6, 4]], Operation.Add, 5)
board.add_group([[5, 4], [5, 5]], Operation.Add, 7)
board.add_group([[6, 5], [6, 6]], Operation.Add, 5)

board.add_permutations()

N = 0


def t(g, p) -> Union[List[int], bool]:
    global N
    N += 1
    valid = board.try_permutation(g, p)

    if valid:
        if g == len(board.groups) - 1:
            return [[g, p]]
        next_group = t(g+1, 0)
        if next_group:
            next_group.append([g, p])
            return next_group
        if not next_group:
            board.reset(g)
    if p == len(board.groups[g].permutations) - 1:
        return False
    return t(g, p+1)


solution = t(0, 0)
print("Found valid board in", N, "tries")
print(board)
print(board.is_valid())
print(board.all_valid())
#print(board._active)

N = 0
board.reset()
for sol in solution:
    g_i = sol[0]
    permutations = board.groups[g_i].permutations
    p_i = sol[1]
    permutations.append(permutations.pop(p_i))
    #permutations.reverse()

board.groups.reverse()

solution = t(0, 0)
print("Found valid board in", N, "tries")
print(board)
print(board.is_valid())
print(board.all_valid())
#print(board._active)
