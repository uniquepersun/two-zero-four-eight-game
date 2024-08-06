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

    def merge(self, row):
        for i in range(3):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def reverse_rows(self, board):
        return [row[::-1] for row in board]

    def transpose(self, board):
        return [list(row) for row in zip(*board)]

    def print_board(self):
        print("Score: {}".format(self.score))
        for row in self.board:
            print("|", end="")
            for tile in row:
                if tile == 0:
                    print("{:4}".format("."), end="")
                else:
                    print("{:4}".format(tile), end="")
            print("|")
        print()

    def check_game_over(self):
        game_over = True
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    game_over = False
                    break
                if j < 3 and self.board[i][j] == self.board[i][j + 1]:
                    game_over = False
                    break
                if i < 3 and self.board[i][j] == self.board[i + 1][j]:
                    game_over = False
                    break
        if game_over:
            print("Game Overrr! your score is: {}".format(self.score))

if __name__ == "__main__":
    game = Game2048()
    directions = {"w": "up", "s": "down", "a": "left", "d": "right"}
    while True:
        move = input("Enter move (w/s/a/d) or 'q' to quit: ").lower()
        if move == "q":
            break
        if move in directions:
            game.move(directions[move])
        else:
            print("Invalid input. Please enter w, s, a, or d.")
