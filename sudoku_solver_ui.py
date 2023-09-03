import tkinter as tk
from sudoku_solver import SudokuSolver
from tkinter import messagebox
from tkinter import simpledialog
import sudoku_generator


class SudokuSolverUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku Solver")
        self.root.geometry(f"{365}x{470}")
        self.root.attributes("-fullscreen", False)

        # Create the content frame
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill="both")

        # Create Dropdown button
        self.dropdown_button = tk.Button(self.root, text="Menu", command=self.show_dropdown)
        self.dropdown_button.pack(anchor="nw")

        # Initialize the dropdown menu
        self.dropdown_menu = tk.Menu(self.root, tearoff=0)
        self.dropdown_menu.add_command(label="Genrate Sudoku", command=self.generate_sudoku)
        self.dropdown_menu.add_command(label="Function 2", command=self.function2)
        self.dropdown_menu.add_command(label="Function 3", command=self.function3)

        # Create padding around the 9x9 grid
        padding_frame = tk.Frame(self.root, padx=10, pady=20)
        padding_frame.pack()


        # Create 9x9 grid of Entry widgets
        vcmd = (self.root.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entries = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(padding_frame, width=2, font=("Helvetica", 20, "bold"), justify='center', validate='key', validatecommand=vcmd)
                entry.grid(row=i, column=j, padx=1, pady=1)
                row.append(entry)
            self.entries.append(row)
        

        # Create Solve button
        solve_button = tk.Button(self.root, text="Solve", command=self.solve_sudoku)
        solve_button.pack()

        # Create Clear button
        clear_button = tk.Button(self.root, text="Clear", command=self.clear_grid)
        clear_button.pack()


        # Bind the <Configure> event to handle resizing
        self.root.bind('<Configure>', self.on_configure)

        # Start the main loop
        self.root.mainloop()
    
    def show_dropdown(self):
        self.dropdown_menu.post(self.dropdown_button.winfo_rootx(), self.dropdown_button.winfo_rooty() + self.dropdown_button.winfo_height())
    
    def generate_sudoku(self):
        difficulty = simpledialog.askinteger("Difficulty", "Enter a number from 0 to 100 for difficulty:")
        empty_squares = 64
        if difficulty is not None:
            if 0 <= difficulty:
                if difficulty < 100:
                    difficulty = 100
                    empty_squares = round(64 * difficulty / 100)
            else:
                tk.messagebox.showerror("Invalid Input", "Please enter a number from 0 to 100.")
        self.update_ui(sudoku_generator.generate_sudoku(empty_squares))
        
    def function2(self):
        pass
    
    def function3(self):
        pass
    
    def clear_grid(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)
    
    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if action == "0":
            return True

        if value_if_allowed and index == "0":
            try:
                n = float(value_if_allowed)
                if n == 0:
                    return False
                return True
            except ValueError:
                return False
        else:
            return False

    def maintain_aspect_ratio(self, event):
        # Calculate the desired width and height based on the aspect ratio
        aspect_ratio = 2.0 / 1.0  # Example aspect ratio: 2:1
        desired_width = event.width
        desired_height = int(desired_width / aspect_ratio)

        # Check if the desired height exceeds the available height
        if desired_height > event.height:
            desired_height = event.height
            desired_width = int(desired_height * aspect_ratio)

        # Place the content frame with the desired dimensions
        for row in self.entries:
            for entry in row:
                entry.config(width=desired_width, height=desired_height)
                entry.geiometry(f"{desired_width}x{desired_height}")

    def calculate_font_size(self):
        # Get the current width and height of the root window
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Calculate the font size based on the window height
        font_size = int((height - 20) * 0.03)  # Adjust the scaling factor as needed

        return font_size
    
    def calculate_entry_size(self):
        # Get the current width and height of the root window
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Calculate the size of each Entry widget based on the window size
        entry_size = int(min(width, height) * 0.08)  # Adjust the scaling factor as needed

        return entry_size
    
    def on_configure(self, event):
        # self.maintain_aspect_ratio(event)

        # Update the font size of Entry widgets when the window is resized
        '''
        font_size = self.calculate_font_size()
        entry_size = self.calculate_entry_size()
        for row in self.entries:
            for entry in row:
                entry.config(font=("Helvetica", font_size))
                '''
    
    # Solve the Sudoku puzzle
    def solve_sudoku(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.entries[i][j].get()
                if value.isdigit() and 1 <= int(value) <= 9:
                    row.append(int(value))
                else:
                    row.append(0)
            board.append(row)

        if self.is_valid_sudoku(board):
            solver = SudokuSolver(board)
            if solver.has_unique_solution():
                board = solver.solutions_list[0]
                self.update_ui(board)
            else:
                messagebox.showerror("Sudoku Solver", "No unique solution!")
        else:
            messagebox.showerror("Sudoku Solver", "Invalid Sudoku!")

    # Check if the given list contains duplicates (except for 0)
    def has_duplicates(self, lst):
        unique_set = set()
        for element in lst:
            if element != 0:
                if element in unique_set:
                    return True
                unique_set.add(element)
        return False

    # Check if the given board is a valid Sudoku board (no duplicates)
    def is_valid_sudoku(self, board):
        # Check rows
        for row in board:
            if self.has_duplicates(row):
                return False

        # Check columns
        for j in range(9):
            column = [board[i][j] for i in range(9)]
            if self.has_duplicates(column):
                return False

        # Check 3x3 board
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                board_3x3 = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                if self.has_duplicates(board_3x3):
                    return False

        return True
    
    # Update the UI with the given board
    def update_ui(self, board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(board[i][j]))

if __name__ == "__main__":
    SudokuSolverUI()

    
