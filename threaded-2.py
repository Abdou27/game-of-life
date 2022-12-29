import tkinter as tk
import threading as th
import random

PIXEL_SIZE = 600
GRID_SIZE = 10
COLOR = "green"
STEP = PIXEL_SIZE / GRID_SIZE


class GameOfLife(tk.Tk):
    def __init__(self):
        super().__init__()
        self.barrier = th.Barrier(GRID_SIZE ** 2)
        self.barrier_refresh = th.Barrier(GRID_SIZE ** 2, action=self.update_grid)
        self.title("Game of Life")
        self.geometry("%dx%d" % (PIXEL_SIZE, PIXEL_SIZE))
        self.game_state = [[random.choice([0, 1]) for _ in range(GRID_SIZE + 2)] for _ in range(GRID_SIZE + 2)]
        self.game_state_neighbors = [[0 for _ in range(GRID_SIZE + 2)] for _ in range(GRID_SIZE + 2)]
        self.canvas = tk.Canvas(self)
        self.init_grid()
        self.update_grid()
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                th.Thread(target=self.recalculate_game_state_case, args=(row + 1, column + 1)).start()

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

    def recalculate_game_state_case(self, i, j):
        while True:
            self.game_state_neighbors[i][j] = sum([
                self.game_state[i - 1][j - 1],
                self.game_state[i - 1][j],
                self.game_state[i - 1][j + 1],
                self.game_state[i][j - 1],
                self.game_state[i][j + 1],
                self.game_state[i + 1][j - 1],
                self.game_state[i + 1][j],
                self.game_state[i + 1][j + 1],
            ])
            self.barrier.wait()
            if self.game_state[i][j] == 0 and self.game_state_neighbors[i][j] == 3:
                self.game_state[i][j] = 1
            elif self.game_state[i][j] == 1 and self.game_state_neighbors[i][j] not in [2, 3]:
                self.game_state[i][j] = 0
            self.barrier_refresh.wait()


window = GameOfLife()
window.mainloop()
