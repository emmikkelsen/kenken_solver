from kenken_solver.board import Board
from kenken_solver.location import Location
from kenken_solver.operation import Operation

N = 9
board = Board(N)


def add(loc_string: str, operation: Operation, result: int):
    """
    Add a group to the board using shorthand notation
    """
    global board
    location_array = []
    for i in range(0, len(loc_string), 2):
        h = ord(loc_string[i]) - 97
        v = int(loc_string[i+1]) - 1
        location_array.append(Location(h, v))
    board.add_group_to_board(location_array, operation, result)


add("a1b1", Operation.SUBTRACT, 8)
add("c1d1", Operation.SUBTRACT, 5)
add("e1f1g1g2", Operation.ADD, 17)
add("h1i1", Operation.SUBTRACT, 1)

add("a2a3b3", Operation.MULTIPLY, 24)
add("b2c2", Operation.ADD, 9)
add("d2e2f2", Operation.ADD, 19)
add("h2i2i3", Operation.ADD, 12)

add("c3c4b4", Operation.MULTIPLY, 252)
add("d3d4", Operation.DIVIDE, 4)
add("e3e4", Operation.ADD, 13)
add("f3g3", Operation.DIVIDE, 4)
add("h3h4", Operation.MULTIPLY, 63)

add("a4a5b5c5", Operation.MULTIPLY, 450)
add("f4f5f6e6", Operation.ADD, 24)
add("g4g5", Operation.SUBTRACT, 3)
add("i4i5", Operation.SUBTRACT, 1)

add("d5e5", Operation.SUBTRACT, 5)
add("h5", Operation.ADD, 4)

add("a6a7", Operation.SUBTRACT, 3)
add("b6b7", Operation.ADD, 17)
add("c6d6", Operation.MULTIPLY, 6)
add("g6g7", Operation.SUBTRACT, 2)
add("h6h7", Operation.MULTIPLY, 8)
add("i6i7", Operation.ADD, 11)

add("c7d7", Operation.SUBTRACT, 5)
add("e7e8d8", Operation.ADD, 21)
add("f7f8", Operation.SUBTRACT, 5)

add("a8a9", Operation.DIVIDE, 2)
add("b8b9", Operation.SUBTRACT, 5)
add("c8c9", Operation.SUBTRACT, 3)
add("g8g9f9", Operation.MULTIPLY, 81)
add("h8i8h9i9", Operation.ADD, 20)

add("d9e9", Operation.MULTIPLY, 10)

board.add_permutations()

solution = board.solve()
print("Found valid board in", board.iterations, "iterations")
print(board)
print("Board is valid" if board.board_is_valid() else "BOARD IS INVALID!")
print("All groups are valid"
      if board.all_groups_valid()
      else "NOT ALL GROUPS VALID!")

print()

board.reset_board()
solution = board.solve_recursive()
print("Found valid board in",
      board.iterations,
      "iterations using recursion")
print(board)
print("Board is valid" if board.board_is_valid() else "BOARD IS INVALID!")
print("All groups are valid"
      if board.all_groups_valid()
      else "NOT ALL GROUPS VALID!")
