"""
Implementation of Conway’s Game of Life
By Chengyuan Sha
"""

import numpy as np

# class to implement Conway’s Game of Life
class Game:
    def __init__(self, input, width, height):
        self.board = self.create_board(input, width, height)
        self.width = width
        self.height = height

    # create a boolean board
    def create_board(self, input, width, height):
        active_position = []
        for x, row in enumerate(input):
            for y, cell in enumerate(row.strip()): # remove possible space
                if cell == "1":
                    active_position.append((x, y))
        board = [[False] * width for _ in range(height)]
        for x, y in active_position:
            board[x][y] = True
        return board

    # create a new board in the new generation
    def update(self):
        new_board = [[False] * self.width for _ in range(self.height)]
        for x, row in enumerate(self.board):
            for y, cell in enumerate(row):
                neighbours = self.count_neighbours(x, y)
                previous_state = self.board[x][y]
                live = (neighbours == 3) or (neighbours == 2 and previous_state == True)
                new_board[x][y] = live
            # update the board
        self.board = new_board
        return self

    # check 9 neighbors
    def count_neighbours(self, x, y):
        count = 0
        for horizontal in [-1, 0, 1]:
            for vertical in [-1, 0, 1]:
                new_horizontal = horizontal + x
                new_vertical = vertical + y
                if (not (horizontal == 0 and vertical == 0)) and (0 <= new_vertical < self.width and 0 <= new_horizontal < self.height):
                    if self.board[new_horizontal][new_vertical] == True:
                        count += 1
        return count

    # get the current board data
    def get_board_data(self):
        data = []
        line = ""
        for x, row in enumerate(self.board):
            for y, cell in enumerate(row):
                if self.board[x][y]:
                    line += "1"
                else:
                    line += "0"
            data.append(line)
            line = ""
        return data

class Main:
    def __init__(self):
        self.h = 0
        self.w = 0
        self.gen_data = []

    def readfile(self, f_name):
        input = np.loadtxt(f_name, skiprows=1, dtype=str)
        gen = np.loadtxt(f_name, max_rows=1, dtype=int)
        # width is the number of columns, height is the number of rows
        width = len(input[0])
        height = len(input)
        if (width < 4 or width > 100) or (height < 4 or height >100):
            raise ValueError("width and height range should be in between 4 and 100. ")
        self.w = width
        self.h = height
        game = Game(input, width=self.w, height=self.h)
        return game, gen

    # output
    def write_file(self, f_name):
        with open(f_name, 'w') as f:
            for i in self.gen_data:
                f.write(i + '\n')

    # run specified generations
    def run(self):
        conways_game, gens = self.readfile("inLife.txt")
        for gen in range(gens+1):
            self.gen_data.append("Generation " + str(gen))
            board = conways_game.get_board_data()
            for i in board:
                self.gen_data.append(i)
            conways_game.update()
        self.write_file('outLife.txt')

if __name__ == "__main__":
    conway = Main()
    conway.run()