import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox 


class SudokuSolverUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.attributes("-fullscreen", False)
        root.geometry(f"{360}x{440}")

        # Create padding around the board
        padding_frame = tk.Frame(root, padx=10, pady=20)
        padding_frame.pack(expand=True)

        # Create 9x9 grid of Entry widgets
        vcmd = (root.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entries = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(padding_frame, width=2, font=("Helvetica", 20, "bold"), justify='center', validate='key', validatecommand=vcmd)
                entry.grid(row=i, column=j, padx=1, pady=1)
                row.append(entry)
            self.entries.append(row)

        # Create Solve button
        solve_button = tk.Button(root, text="Solve", command=self.solve_sudoku)
        solve_button.pack()


        # Bind the <Configure> event to handle resizing
        self.root.bind('<Configure>', self.on_configure)
    
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



    def solve_sudoku(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.entries[i][j].get()
                if value.isdigit() and 1 <= int(value) <= 9:
                    row.append(int(value))
                else:
                    row.append(0)
            grid.append(row)

        if self.is_valid_sudoku(grid):
            if self.solve(grid):
                self.update_ui(grid)
                tk.messagebox.showinfo("Sudoku Solver", "Sudoku solved!")
            else:
                tk.messagebox.showerror("Sudoku Solver", "Unable to solve Sudoku!")
        else:
            tk.messagebox.showerror("Sudoku Solver", "Invalid Sudoku!")

    def check_duplicates(self, lst):
        unique_set = set()
        for element in lst:
            if element != 0:
                if element in unique_set:
                    return True
                unique_set.add(element)
        return False

    def is_valid_sudoku(self, grid):
        # Check rows
        for row in grid:
            if self.check_duplicates(row):
                return False

        # Check columns
        for j in range(9):
            column = [grid[i][j] for i in range(9)]
            if self.check_duplicates(column):
                return False

        # Check 3x3 grids
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                grid_3x3 = [grid[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                if self.check_duplicates(grid_3x3):
                    return False

        return True

    def find_empty_location(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return i, j
        return None

    def is_valid_number(self, grid, num, row, col):
        # Check row
        if num in grid[row]:
            return False

        # Check column
        for i in range(9):
            if grid[i][col] == num:
                return False

        # Check 3x3 grid
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == num:
                    return False

        return True

    def solve(self, grid):
        loc = self.find_empty_location(grid)
        if loc is None:
            return True

        row, col = loc
        for num in range(1, 10):
            if self.is_valid_number(grid, num, row, col):
                grid[row][col] = num

                if self.solve(grid):
                    return True

                grid[row][col] = 0

        return False

    def update_ui(self, grid):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(grid[i][j]))


if __name__ == "__main__":
    root = tk.Tk()
    SudokuSolverUI(root)
    root.mainloop()
