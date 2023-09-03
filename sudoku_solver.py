import copy
import time
from sudoku_board import SudokuBoard

class SudokuBaseSolve:
    def __init__(self, board: list[list[int]]):
        self.initial_board = SudokuBoard(board)
        self.board = SudokuBoard(board)
        self.countSolutions = False
        self.recursions = 0
        self.solutions = 0
        self.solutions_list = []
        self.time_taken = 0

    def _find_empty_cell(self) -> tuple:
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if col == 0:
                    return x, y
        return None

    def _is_valid_placement(self, num: int, pos: tuple) -> bool:
        x, y = pos
        if num in self.board[y]:
            return False
        
        colLine = [row[x] for row in self.board]
        if num in colLine:
            return False

        box = [
            self.board[i + (y // 3) * 3][j + (x // 3) * 3]
            for i in range(3)
            for j in range(3)
        ]

        return num not in box
    
    def _reset_board(self):
        self.board = copy.deepcopy(self.initial_board)
        
class SudokuSolver(SudokuBaseSolve):
    def __init__(self, board: list[list[int]]):
        super().__init__(board)

    def has_unique_solution(self):
        self._reset_board()
        self.solve(True)
        return self.solutions == 1
    
    def solve(self, checkForUnique: bool = False):
        self.recursions += 1
        empty = self._find_empty_cell()
        if empty is None:
            self.solutions += 1
            self.solutions_list.append(copy.deepcopy(self.board))
            return True

        if checkForUnique and self.solutions > 1:
            return True
        
        x, y = empty

        for digit in range(1, 10):
            if self._is_valid_placement(digit, (x, y)):
                self.board[y][x] = digit
                if self.solve(checkForUnique):
                    if not self.countSolutions and not checkForUnique:
                        return True
                self.board[y][x] = 0
        return False

    def timed_solve(self):
        start_time = time.time()
        self.solve()
        self.time_taken = time.time() - start_time
        return self.time_taken

class OptimizedSudokuSolver(SudokuBaseSolve):
    def __init__(self, board: list[list[int]]):
        super().__init__(board)

    def _col_form(self):
        return [[row[i] for row in self.board] for i in range(9)]

    def _box_form(self):
        new_board = [
            [self.board[i + box_row * 3][j + box_col * 3]
                for i in range(3)
                for j in range(3)
            ]
            for box_row in range(3)
            for box_col in range(3)
        ]
        return new_board

    def _psbl_form(self):
        for row in range(9):
            for col in range(9):
                if not self.board[row][col]:
                    pos_list = [digit for digit in range(1, 10) if self._is_valid_placement(digit, (col, row))]
                    self.board[row][col] = pos_list

    def _zero_replace(self):
        for row in range(9):
            for col in range(9):
                if isinstance(self.board[row][col], list):
                    self.board[row][col] = 0

    def _fill_line(self, line):
        # Check for single possible values
        replaced_values = set()
        for i, pos in enumerate(line):
            if isinstance(pos, list) and len(pos) == 1:
                line[i] = pos[0]
                replaced_values.add(pos[0])
                
        for num in replaced_values:
            for i, pos in enumerate(line):
                if isinstance(pos, list) and num in pos:
                    pos.remove(num)

        # Check for numbers with only one possible position
        replaced_values = set()
        for num in range(1, 10):
            pos_list = []
            for i, pos in enumerate(line):
                if isinstance(pos, list) and num in pos:
                    pos_list.append(i)
            if len(pos_list) == 1:
                line[pos_list[0]] = num
                replaced_values.add(num)
            
        for num in replaced_values:
            for i, pos in enumerate(line):
                if isinstance(pos, list) and num in pos:
                    pos.remove(num)
                    
    def _fill_board(self):
        # use clasic methods to fill the board as much as possible
        orig_board = []
        while(orig_board != self.board):
            orig_board = copy.deepcopy(self.board)
            self._psbl_form()
            for row in self.board:
                self._fill_line(row)
            for col in self._col_form():
                self._fill_line(col)
            for box in self._box_form():
                self._fill_line(box)
            self._zero_replace()
        
    def solve(self) -> bool:
        self.recursions += 1
        prev_state = copy.deepcopy(self.board)
        self._fill_board()

        empty_cell = self._find_empty_cell()
        if not empty_cell:
            return True
        
        x, y = empty_cell
        
        for num in range(1, 10):
            if self._is_valid_placement(num, (x, y)):
                self.board[y][x] = num
                
                if self.solve():
                    return True

                self.board[y][x] = 0
                self.board = copy.deepcopy(prev_state) 

        return False
    
    def timed_solve(self):
        start_time = time.time()
        self.solve()
        self.time_taken = time.time() - start_time
        return self.time_taken

        
if __name__ == "__main__":
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


    solver = SudokuSolver(board)
    solver.timed_solve()
    print(solver.board)
    print(f"recursions: {solver.recursions}, time: {solver.time_taken}, solutions: {solver.solutions}")
    
    
    print("Optimized:")
    solver = OptimizedSudokuSolver(board)
    solver.timed_solve()
    print(solver.board)
    print(f"recursions: {solver.recursions}, time: {solver.time_taken}")