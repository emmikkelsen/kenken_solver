from kenken_solver.board import Board
from kenken_solver.operation import Operation

N = 9
board = Board(N)


def add(loc_string: str, op: Operation, result: int):
    """
    Add a group to the board using shorthand notation
    """
    global board
    location_array = []
    for i in range(0, len(loc_string), 2):
        h = ord(loc_string[i]) - 97
        v = int(loc_string[i+1]) - 1
        location_array.append([h, v])
    board.add_group_to_board(location_array, op, result)


add("a1b1", Operation.Subtract, 8)
add("c1d1", Operation.Subtract, 5)
add("e1f1g1g2", Operation.Add, 17)
add("h1i1", Operation.Subtract, 1)

add("a2a3b3", Operation.Multiply, 24)
add("b2c2", Operation.Add, 9)
add("d2e2f2", Operation.Add, 19)
add("h2i2i3", Operation.Add, 12)

add("c3c4b4", Operation.Multiply, 252)
add("d3d4", Operation.Divide, 4)
add("e3e4", Operation.Add, 13)
add("f3g3", Operation.Divide, 4)
add("h3h4", Operation.Multiply, 63)

add("a4a5b5c5", Operation.Multiply, 450)
add("f4f5f6e6", Operation.Add, 24)
add("g4g5", Operation.Subtract, 3)
add("i4i5", Operation.Subtract, 1)

add("d5e5", Operation.Subtract, 5)
add("h5", Operation.Add, 4)


add("a6a7", Operation.Subtract, 3)
add("b6b7", Operation.Add, 17)
add("c6d6", Operation.Multiply, 6)
add("g6g7", Operation.Subtract, 2)
add("h6h7", Operation.Multiply, 8)
add("i6i7", Operation.Add, 11)

add("c7d7", Operation.Subtract, 5)
add("e7e8d8", Operation.Add, 21)
add("f7f8", Operation.Subtract, 5)

add("a8a9", Operation.Divide, 2)
add("b8b9", Operation.Subtract, 5)
add("c8c9", Operation.Subtract, 3)
add("g8g9f9", Operation.Multiply, 81)
add("h8i8h9i9", Operation.Add, 20)

add("d9e9", Operation.Multiply, 10)

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
