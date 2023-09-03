from sudoku_solver import SudokuSolver, OptimizedSudokuSolver
import sudoku_generator as SudokuGenerator
import random
import json

def generate_tests(number_of_tests: int) -> list[list[list[int]]]:
    board_list = []
    for _ in range(number_of_tests):
        difficulty = random.randint(40, 70)
        board = SudokuGenerator.generate_sudoku(difficulty)
        board_list.append(board)
    return board_list

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data

if __name__ == "__main__":    
    # Load tests from file
    loaded_results = load_from_file("sudoku_tests.json")
    
    basic_times = []
    optimized_times = []
    
    for board in loaded_results:
        basic_times.append(SudokuSolver(board).timed_solve())
        optimized_times.append(OptimizedSudokuSolver(board).timed_solve())
    
    print("Basic solver average time: ", sum(basic_times) / len(basic_times))
    print("Optimized solver average time: ", sum(optimized_times) / len(optimized_times))
    
    