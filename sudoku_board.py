import copy

class SudokuBoard:
    def __init__(self, board: list[list[int]]):
        self.board = copy.deepcopy(board)
    
    def __getitem__(self, index):
        return self.board[index]
    
    def __setitem__(self, index, value):
        self.board[index] = value
    
    def __len__(self):
        return len(self.board)
    
    def __iter__(self):
        return iter(self.board)
    
    def __delitem__(self, index):
        del self.board[index]
    
    def __contains__(self, item):
        return item in self.board

    def __deepcopy__(self, memo):
        return SudokuBoard(copy.deepcopy(self.board, memo))

    def __repr__(self):
        return str(self.board)
    
    def __eq__(self, other):
        if isinstance(other, SudokuBoard):
            return self.board == other.board
        elif isinstance(other, list):
            return self.board == other
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        board_str = ""
        for row in self.board:
            for col in row:
                num = col if col != 0 else "."
                board_str += str(num) + " "
            board_str += "\n"
        return board_str
    
    def print_board(self):
        for row in range(len(self.board)):
            if row % 3 == 0 and row != 0:
                print("- - - - - - - - - - - - - ")
            for col in range(len(self.board[0])):
                if col % 3 == 0 and col != 0:
                    print(" | ", end="")
                if col == 8:
                    print(str(self.board[row][col]))
                else:
                    print(str(self.board[row][col]) + " ", end="")