import random
import numpy
import readchar
import os
from termcolor import colored
# import tkinter as tk

class Game_2048(object):

    MOVE_DICT = {"w": "up", "a": "left", "s": "down", "d": "right"}
    ARROW_DICT = {'\x00H' : "up", '\x00P' : "down", '\x00M' : "right", '\x00K' : "left",
                  '^[[A' : "up", '^[[B' : "down", '^[[C' : "right", '^[[D' : "left"  }
    COLOR_DICT = {0: "white", 2: "red", 4: "light_red", 8: "magenta", 16: "light_magenta", 32: "yellow", 64: "light_yellow", 128: "green", 256: "light_green", 512: "cyan", 1024: "light_cyan", 2048: "blue"}

    def __init__(self, dim):
        self.size = dim
        self.board = [[0 for i in range(dim)] for j in range(dim)]
        self.move = None

    def get_board(self):
        return self.board

    def copy(self):
        return [[i for i in self.board[j]] for j in range(self.size)]
    
    def game_won(self):
        for row in self.board:
            if 2048 in row:
                return True
        return False
    
    def legal_moves(self):
        output = []
        for row in range(self.size):
            for cell in range(self.size):
                if self.board[row][cell] != 0:
                    if row + 1 < self.size:
                        if self.board[row][cell] == self.board[row + 1][cell] or self.board[row + 1][cell] == 0:
                            if "down" not in output:
                                output.append("down")
                                if len(output) == 4:
                                    return output
                    if row - 1 >= 0:
                        if self.board[row][cell] == self.board[row - 1][cell] or self.board[row - 1][cell] == 0:
                            if "up" not in output:
                                output.append("up")
                                if len(output) == 4:
                                    return output
                    if cell + 1 < self.size:
                        if self.board[row][cell] == self.board[row][cell + 1] or self.board[row][cell + 1] == 0:
                            if "right" not in output:
                                output.append("right")
                                if len(output) == 4:
                                    return output
                    if cell - 1 >= 0:
                        if self.board[row][cell] == self.board[row][cell - 1] or self.board[row][cell - 1] == 0:
                            if "left" not in output:
                                output.append("left")
                                if len(output) == 4:
                                    return output
        return output
    
    def perform_move(self):
        if self.move == "up":
            self.move_up()
        elif self.move == "down":
            self.move_down()
        elif self.move == "left":
            self.move_left()
        elif self.move == "right":
            self.move_right()

    def move_up(self):
        self.board = numpy.transpose(self.board)
        self.move_left()
        self.board = numpy.transpose(self.board)

    def move_down(self):
        self.board = numpy.transpose(self.board)
        self.move_right()
        self.board = numpy.transpose(self.board)

    def move_left(self):
        output = []
        row_counter = 0
        for row in self.board:
            for index in range(0, self.size):
                if row[index] != 0:
                    for jump in range(1, self.size):
                        keep_going = True
                        if index - jump >= 0:
                            if row[index - jump] == 0 and index - jump == 0:
                                row[index - jump] = row[index]
                                row[index] = 0
                                keep_going = False
                            elif row[index - jump] == row[index]:
                                row[index] = 0
                                row[index - jump] = row[index - jump] * 2
                                keep_going = False
                            elif row[index - jump] == 0:
                                pass
                            elif row[index - jump] > 0:
                                keep_going = False
                                if index - jump + 1 < index:
                                    row[index - jump + 1] = row[index] 
                                    row[index] = 0
                                else:
                                    pass
                            else:
                                raise("IDK WHAT HAPPENED")
                        if not keep_going:
                            break
            output.append(row)
            row_counter += 1
        self.board = output

    def move_right(self):
        output = []
        row_counter = 0
        for row in self.board:
            for index in range(0, self.size)[::-1]:
                if row[index] != 0:
                    for jump in range(1, self.size):
                        keep_going = True
                        if index + jump < self.size:
                            if row[index + jump] == 0 and index + jump + 1 == self.size:
                                row[index + jump] = row[index]
                                row[index] = 0
                                keep_going = False
                            elif row[index + jump] == row[index]:
                                row[index] = 0
                                row[index + jump] = row[index + jump] * 2
                                keep_going = False
                            elif row[index + jump] == 0:
                                pass
                            elif row[index + jump] > 0:
                                keep_going = False
                                if index + jump - 1 > index:
                                    row[index + jump - 1] = row[index] 
                                    row[index] = 0
                                else:
                                    pass
                            else:
                                raise("IDK WHAT HAPPENED")
                        if not keep_going:
                            break
            output.append(row)
            row_counter += 1
        self.board = output

    def number_of_blanks(self):
        count = 0
        output = []
        for row_i in range(self.size):
            for tile_i in range(self.size):
                if self.board[row_i][tile_i] == 0:
                    count += 1
                    output.append((row_i, tile_i))
        return (count, output)
        
    def add_random_tile(self):
        tile_info = self.number_of_blanks()
        open_tiles = tile_info[1]
        random_tile = random.choice(open_tiles)
        self.board[random_tile[0]][random_tile[1]] = random.choice([2, 4])
        
    def __str__(self):
        out = ""
        for row in self.board:
            rowstr = ""
            for item in row:
                rowstr += colored(str(item), self.COLOR_DICT[item]) + "  "
            out += rowstr + "\n"
        return out
    
    def terminal_game_launcher(self):
        while self.number_of_blanks()[0] != 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.add_random_tile()
            print(self)
            if self.legal_moves():
                not_satisfied = True
                print("\nPerform moves with arrow keys")
                while not_satisfied:
                    move = readchar.readkey()
                    if self.ARROW_DICT[move] in self.legal_moves():
                        self.move = self.ARROW_DICT[move]
                        self.perform_move()
                        not_satisfied = False
                        if self.game_won():
                            print("\nYou win!\n")
                            quit()
                    else:
                        pass
        print("Game over")
                    
if __name__ == "__main__":
    Game_2048(4).terminal_game_launcher()