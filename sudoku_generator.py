import random
import sudoku_solver as sSolver

def generate_sudoku(difficulty):
    grid = [[0 for _ in range(9)] for _ in range(9)]
    empty_squares = difficulty

    __fill_diagonal(grid)
    __fill_grid_random(grid)

    posion = []
    if empty_squares > 0:
        for row in range(9):
            for col in range(9):
                posion.append((row, col))
    
    random.shuffle(posion)

    while empty_squares > 0 and len(posion) > 0:
        row, col = posion.pop()

        while grid[row][col] == 0:  # find a filled cell
            row = random.randint(0, 8)
            col = random.randint(0, 8)

        backup = grid[row][col]
        grid[row][col] = 0

        if sSolver.SudokuSolver().unique_solution(grid):
            empty_squares -= 1
        else:
            grid[row][col] = backup  # put the last cell value back
    
    print(81 - difficulty + empty_squares)
    return grid

def __is_valid(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False

    for x in range(9):
        if grid[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False

    return True

def __fill_grid_random(grid, row=0, col=0):
    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0

    if grid[row][col] > 0:
        return __fill_grid_random(grid, row, col + 1)

    for num in __shuffle_numbers():
        if __is_valid(grid, row, col, num):
            grid[row][col] = num

            if __fill_grid_random(grid, row, col + 1):
                return True

        grid[row][col] = 0

    return False

def __shuffle_numbers():
    numbers = list(range(1, 10))
    random.shuffle(numbers)
    return numbers

# fill the diagonal 3x3 box
def __fill_diagonal(grid):
    for box_corner in range(0, 9, 3):
        # fill 3x3 box
        val = __shuffle_numbers()
        for i in range(3):
            for j in range(3):
                grid[box_corner + i][box_corner + j] = val.pop()


def print_sudoku(grid):
    for i in range(9):
        for j in range(9):
            print(grid[i][j], end=' ')
        print()

def calculate_prevalence(grids):
    prevalence_chart = {}
    total_grids = len(grids)

    for row in range(9):
        for col in range(9):
            slot_prevalence = {}

            for num in range(0, 10):
                num_count = sum(1 for grid in grids if grid[row][col] == num)
                slot_prevalence[num] = round((num_count / total_grids) * 100)

            prevalence_chart[(row, col)] = slot_prevalence

    return prevalence_chart


if __name__ == '__main__':
    # print_sudoku(generate_sudoku(0))  # The number represents the number of squares that will be emptied. 
    x = []
    for i in range(100000):
        x.append(generate_sudoku(40))
    
    print(calculate_prevalence(x))