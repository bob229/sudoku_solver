import copy

import rec_recorder


# Finds the next empty box
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


# Gives list of all possible digits for each empty square with nested list
def psbl_form(bo):
    for row in range(len(bo)):
        for col in range(len(bo[0])):
            if not bo[row][col]:
                pos_list = []
                for digit in range(1, 10):
                    if valid(bo, digit, (row, col)):
                        pos_list.append(digit)
                bo[row][col] = pos_list
    return bo


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


# Replaces possibilities with 0
def zero_replace(bo):
    for row in range(len(bo)):
        for col in range(len(bo[0])):
            if type(bo[row][col]) is list:
                bo[row][col] = 0


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


# Takes a line in psbl_form and number being checked
def line_replace(line, num, pos=8, count=0):
    if pos == -1:
        return count

    if type(line[pos]) is not list:
        count = line_replace(line, num, pos - 1, count)
        return count

    if num in line[pos]:
        count += 1
        count = line_replace(line, num, pos - 1, count)
        if count == 1:
            line[pos] = num
            return count
        else:
            return count
    else:
        count = line_replace(line, num, pos - 1, count)
        return count


def experimental_solve(bo):
    while True:
        orig_bo = copy.deepcopy(bo)
        psbl_form(bo)
        for row in range(len(bo)):
            for num in range(10):
                line_replace(bo[row], num)

        zero_replace(bo)
        psbl_form(bo)
        col_board = col_form(bo)
        for col in range(len(col_board)):
            for num in range(10):
                line_replace(col_board[col], num)
        zero_replace(col_board)
        bo = col_form(col_board)
        if orig_bo == bo:
            break
    return bo
