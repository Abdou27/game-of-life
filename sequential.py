import tkinter as tk
import threading as th
import random

PIXEL_SIZE = 600
GRID_SIZE = 10
REFRESH_RATE = 60
COLOR = "green"
STEP = PIXEL_SIZE / GRID_SIZE


class GameOfLife(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game of Life")
        self.geometry("%dx%d" % (PIXEL_SIZE, PIXEL_SIZE))
        self.game_state = [[random.choice([0, 1]) for _ in range(GRID_SIZE + 2)] for _ in range(GRID_SIZE + 2)]
        self.game_state_neighbors = [[0 for _ in range(GRID_SIZE + 2)] for _ in range(GRID_SIZE + 2)]
        self.canvas = tk.Canvas(self)
        self.init_grid()
        self.update_grid()

    def init_grid(self):
        for i in range(GRID_SIZE):
            self.canvas.create_line(i * STEP, 0, i * STEP, PIXEL_SIZE)
            self.canvas.create_line(0, i * STEP, PIXEL_SIZE, i * STEP)

    def update_grid(self):
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                fill_color = COLOR if self.game_state[row + 1][column + 1] == 1 else "white"
                self.canvas.create_rectangle(column * STEP, row * STEP, (column + 1) * STEP, (row + 1) * STEP,
                                             fill=fill_color)

        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.recalculate_game_state()
        self.after(int(1000 / REFRESH_RATE), self.update_grid)

    def recalculate_game_state(self):
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                self.game_state_neighbors[row + 1][column + 1] = sum([
                    self.game_state[row][column],
                    self.game_state[row][column + 1],
                    self.game_state[row][column + 2],
                    self.game_state[row + 1][column],
                    self.game_state[row + 1][column + 2],
                    self.game_state[row + 2][column],
                    self.game_state[row + 2][column + 1],
                    self.game_state[row + 2][column + 2],
                ])
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                if self.game_state[row + 1][column + 1] == 0 and self.game_state_neighbors[row + 1][column + 1] == 3:
                    self.game_state[row + 1][column + 1] = 1
                elif self.game_state[row + 1][column + 1] == 1 and self.game_state_neighbors[row + 1][column + 1] not in [2, 3]:
                    self.game_state[row + 1][column + 1] = 0



window = GameOfLife()
window.mainloop()
