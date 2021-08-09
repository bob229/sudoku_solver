import time
import copy
import rec_solve as rec
import experimental_solve as exp
import rec_recorder

board = [
  [8, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 3, 6, 0, 0, 0, 0, 0],
  [0, 7, 0, 0, 9, 0, 2, 0, 0],
  [0, 5, 0, 0, 0, 7, 0, 0, 0],
  [0, 0, 0, 0, 4, 5, 7, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 3, 0],
  [0, 0, 1, 0, 0, 0, 0, 6, 8],
  [0, 0, 8, 5, 0, 0, 0, 1, 0],
  [0, 9, 0, 0, 0, 0, 4, 0, 0]
]

board_exp = copy.deepcopy(board)


# Prints the board
def print_board(bo):
    for row in range(len(bo)):
        if row % 3 == 0 and row != 0:
            print("- - - - - - - - - - - - - ")
        for col in range(len(bo[0])):
            if col % 3 == 0 and col != 0:
                print(" | ", end="")
            if col == 8:
                print(str(bo[row][col]))
            else:
                print(str(bo[row][col]) + " ", end="")


# Regular solve
rec_recorder.recursions = 0
print("Board:")
print_board(board)

print("Regular reclusive solve Board:")
start = time.time()

rec.rec_solve(board)

end = time.time()
print("Time(s):", end - start)
print("Recursions:", rec_recorder.recursions)
print_board(board)

# Experimental solve
rec_recorder.recursions = 0
print("Experimental solve Board:")
start = time.time()
board_exp = exp.experimental_solve(board_exp)
print_board(board_exp)

print("Solve /w experimental Board:")
exp.rec_solve(board_exp)
end = time.time()
print("Time(s):", end - start)
print("Recursions:", rec_recorder.recursions)
print_board(board_exp)
