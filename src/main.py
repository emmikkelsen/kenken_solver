from kenken_solver.board import Board
from kenken_solver.operation import Operation

N = 9
board = Board(N)


def add(loc_string: str, op: Operation, result: int):
    global board
    location_array = []
    for i in range(0, len(loc_string), 2):
        h = ord(loc_string[i]) - 97
        v = int(loc_string[i+1]) - 1
        location_array.append([h, v])
    board.add_group_to_board(location_array, op, result)


add("a1b1", Operation.Subtract, 1)
add("c1d1", Operation.Subtract, 3)
add("e1", Operation.Add, 7)
add("f1g1", Operation.Add, 14)
add("h1", Operation.Add, 1)
add("i1i2", Operation.Subtract, 7)

add("a2b2c2d2", Operation.Add, 21)
add("e2f2e3e4", Operation.Add, 14)
add("g2g3", Operation.Add, 10)
add("h2h3i3i4", Operation.Add, 19)

add("a3b3", Operation.Add, 17)
add("c3d3", Operation.Subtract, 3)
add("f3f4", Operation.Subtract, 2)

add("a4a5", Operation.Subtract, 1)
add("b4c4", Operation.Subtract, 6)
add("d4d5", Operation.Subtract, 1)
add("g4g5f5", Operation.Add, 14)
add("h4h5i5", Operation.Add, 16)

add("b5", Operation.Add, 7)
add("c5c6d6", Operation.Add, 8)
add("e5e6e7", Operation.Add, 16)

add("a6b6", Operation.Subtract, 5)
add("f6f7", Operation.Subtract, 5)
add("g6g7", Operation.Subtract, 4)
add("h6h7", Operation.Subtract, 1)
add("i6i7", Operation.Add, 14)

add("a7", Operation.Add, 9)
add("b7c7", Operation.Subtract, 5)
add("d7d8", Operation.Add, 3)

add("a8a9b9", Operation.Add, 13)
add("b8c8", Operation.Add, 11)
add("e8e9f8f9", Operation.Add, 27)
add("g8g9", Operation.Add, 10)
add("h8h9", Operation.Add, 10)
add("i8i9", Operation.Subtract, 4)

add("c9d9", Operation.Add, 8)


board.add_permutations()

solution = board.solve()
print("Found valid board in", board.permutations_tried, "tries")
print(board)
print(board.is_valid())
print(board.all_valid())

board.reset_board()
solution = board.solve_recursive()
print("Found valid board in", board.permutations_tried, "tries")
print(board)
print(board.is_valid())
print(board.all_valid())
