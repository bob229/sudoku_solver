class SudokuSolver:
    def __init__(self, countSolutions: bool = False):
        self.countSolutions = countSolutions
        self.uniqueSolution = False
        
        self.recursions = 0
        self.solutions = 0
        self.solutions_list = []
    
    # checks if sudoku grid has one unique solution
    def unique_solution(self, grid: list[list[int]]):
        grid_copy = [line[:] for line in grid]
        self.uniqueSolution = True
        self.solve(grid_copy)
        self.uniqueSolution = False
        return self.solutions == 1

    # Solves sudoku grid using backtracking
    def solve(self, grid: list[list[int]]):
        self.recursions += 1

        empty = self.__find_empty(grid)
        if empty is None:
            if self.countSolutions or self.uniqueSolution:
                self.solutions += 1
                self.solutions_list.append([line[:] for line in grid])
            return True

        x, y = empty

        for digit in range(1, 10):
            if self.__valid_grid(grid, digit, (x, y)):
                grid[y][x] = digit

                if self.solve(grid):
                    if not self.countSolutions and not self.uniqueSolution:
                        return True
                elif self.uniqueSolution and self.solutions > 1:
                    return False

                grid[y][x] = 0
        return False

    # Checks if number is valid
    def __valid_grid(self, grid: list[list[int]], num: int, pos: tuple) -> bool:
        x, y = pos
        if num in grid[y]:
            return False
        colLine = []
        for row in grid:
            colLine.append(row[x])
        if num in colLine:
            return False
        box = []
        for i in range(3):
            for j in range(3):
                box.append(grid[i + (y // 3) * 3][j + (x // 3) * 3])
        if num in box:
            return False

        return True
    
    # Finds empty cell in grid
    def __find_empty(self, grid) -> tuple:
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                if col == 0:
                    return x, y
        return None

class OptimizedSudokuSolver:
    def __init__(self):
        self.heuristic_order
        self.precompute_moves
        self.iterative_backtracking
        self.forward_checking


    # Solves sudoku grid using optimized backtracking
    def optimized_solve(self, grid: list[list[int]]):
        empty = self.find_empty(grid)
        if empty is None:
            return True
        row, col = empty
        for digit in range(1, 10):
            if self.__valid_grid(grid, digit, (row, col)):
                grid[row][col] = digit
                if self.optimized_solve(grid):
                    return True
                grid[row][col] = 0
        return False
    
    # Checks if number is valid
    def __valid_grid(self, grid: list[list[int]], num: int, pos: tuple) -> bool:
        x, y = pos
        if num in grid[y]:
            return False
        colLine = []
        for row in grid:
            colLine.append(row[x])
        if num in colLine:
            return False
        box = []
        for i in range(3):
            for j in range(3):
                box.append(grid[i + (y // 3) * 3][j + (x // 3) * 3])
        if num in box:
            return False

        return True

    # Gives list of all possible digits for each empty square with nested list
    def psbl_form(grid):

        for x, row in enumerate(grid):
            for y, col in enumerate(row):
                if not col:
                    posablities_list = []
                    for digit in range(1, 10):
                        if self.valid(bo, digit, (x, y)):
                            posablities_list.append(digit)
                    bo[row][col] = pos_list
        return bo