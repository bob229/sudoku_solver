import rec_recorder


def find_empty(bo):
    for row in range(len(bo)):
        for col in range(len(bo[0])):
            if bo[row][col] == 0:
                return row, col  # row, col
    return False


# Makes list of sudoku columns
def col_form(bo):
    col_bo = []
    for i in range(len(bo)):
        col = []
        for j in range(len(bo[0])):
            col.append(bo[j][i])
        col_bo.append(col)
    return col_bo  # col, row


# Makes list of sudoku boxes
def box_form(bo):
    new_bo = []
    for box_row in range(3):
        for box_col in range(3):
            box = []
            for i in range(3):
                for j in range(3):
                    box.append(bo[i + box_row * 3][j + box_col * 3])
            new_bo.append(box)
    return new_bo


# Checks if number is valid
def valid(bo, num, pos):  # pos = (row, col)
    col_board = col_form(bo)
    box_board = box_form(bo)

    for i in range(len(bo[pos[0]])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(col_board[pos[1]])):
        if col_board[pos[1]][i] == num and pos[0] != i:
            return False

    current_box = 3 * (pos[0] // 3) + pos[1] // 3

    for i in range(len(box_board[current_box])):
        if box_board[current_box][i] == num and pos[0] != i:
            return False

    return True


# Recursion solve
def rec_solve(bo):
    empty = find_empty(bo)
    if not empty:
        return True
    row, col = empty

    for digit in range(1, 10):
        if valid(bo, digit, (row, col)):
            rec_recorder.recursions += 1
            bo[row][col] = digit

            if rec_solve(bo):
                return True

            bo[row][col] = 0
    return False
