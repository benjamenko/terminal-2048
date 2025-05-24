from Game_2048 import Game_2048
from tkinter import *
from tkinter import ttk
import readchar
import os

class GUI2048(object):

    def __init__(self, size):
        self.game = Game_2048(size)
        self.stored_labels = [[None for _ in range(self.game.size)] for _ in range(self.game.size)]
        self.root = Tk()
        self.root.title("2048 Game")

        # Bind the arrow key events to the function
        while True:
            self.create_grid()
            self.root.after(5, self.game.add_random_tile())
            self.root.bind("<Up>", self.on_key_press("up"))
            self.root.bind("<Down>", self.on_key_press("down"))
            self.root.bind("<Left>", self.on_key_press("left"))
            self.root.bind("<Right>", self.on_key_press("right"))
            # Start the event loop
            self.root.mainloop()
            

    def create_grid(self):
        for i in range(self.game.size):
            for j in range(self.game.size):
                self.LABEL = Label(self.root, text=str(self.game.board[i][j]), width=5, height=2, relief="solid", font=("Helvetica", 16))
                self.LABEL.grid(row=i, column=j+20)
                self.stored_labels[i][j] = self.LABEL

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                self.LABEL = Label(self.root, text=str(self.game.board[i][j]), width=5, height=2, relief="solid", font=("Helvetica", 16))

    def on_key_press(self, event):
        if event == 'up':
            self.game.move = 'up'
            self.game.perform_move()
        elif event == 'down':
            self.game.move = 'down'
            self.game.perform_move()
        elif event == 'left':
            self.game.move = 'left'
            self.game.perform_move()
        elif event== 'right':
            self.game.move = 'right'
            self.game.perform_move()
        self.update_grid()

if __name__ == "__main__":
    GUI2048(4)
