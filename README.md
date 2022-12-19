# KenKen
KenKen is a puzzle game somewhat reminiscent of Sudoku. The board is an N-by-N matrix of squares (I've seen variants only for N>3). Every row and column must contain all numbers from 1-N once and only once.

Furthermore, the board is divided into groups. Each group consists of squares, an operation (addition, subtraction, multiplication, division), and a result. The operation applied to the contents of the group (in any order) must yield the result of the group.

For example, the upper-leftmost group on `sample_board.png` can be solved only by the values (1, 9) and (9, 1) since they are the only numbers that solve A-B=8 for A and B between 1 and 9. See [kenkenpuzzle.com](https://www.kenkenpuzzle.com/game) for more information on gameplay and rules.

This code solves KenKen puzzles. Running `python main.py` in the `src` folder will print the solution to the log. The current puzzle defined in `main.py` is shown on the image in `sample_board.png`. *The code is tested to run on Python 3.7 and 3.10*.
