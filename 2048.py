import random
import copy

class Game2048:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.place_initial_tiles()
        
    def place_initial_tiles(self):
        for _ in range(2):
            self.place_random_tile()

    def place_random_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        prev_board = copy.deepcopy(self.board)
        if direction == "Up":
            self.board = self.transpose(self.board)
            self.board = self.move_left(self.board)
            self.board = self.transpose(self.board)
        elif direction == "Down":
            self.board = self.transpose(self.board)
            self.board = self.reverse_rows(self.board)
            self.board = self.move_left(self.board)
            self.board = self.reverse_rows(self.board)
            self.board = self.transpose(self.board)
        elif direction == "Left":
            self.board = self.move_left(self.board)
        elif direction == "Right":
            self.board = self.reverse_rows(self.board)
            self.board = self.move_left(self.board)
            self.board = self.reverse_rows(self.board)
        
        if self.board != prev_board:
            self.place_random_tile()
            self.print_board()
            self.check_game_over()

    def move_left(self, board):
        new_board = []
        for row in board:
            new_row = self.compress(row)
            new_row = self.merge(new_row)
            new_row = self.compress(new_row)
            new_board.append(new_row)
        return new_board

    def compress(self, row):
        new_row = [0] * 4
        index = 0
        for value in row:
            if value != 0:
                new_row[index] = value
                index += 1
        return new_row

