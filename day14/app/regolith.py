# regolith.py

import numpy
import logging

logging.basicConfig(level=logging.INFO)


class Regolith:
    EMPTY = 0
    WALL = 1
    SOURCE = 2
    OCCUPIED = 3

    def __init__(self):
        self.rock = self.read_input("/home/mixlmay/Code/Python/AoC2022/day14/input_day14.txt")
        self.initial_grid = self.generate_initial_grid()
    def read_input(self, filename: str) -> []:
        with open(filename, "r") as fs:
            input = [[[int(i) for i in pair.strip().split(',')] for pair in line.split(" -> ")] for line in fs]
        return input

    def generate_initial_grid(self):
        logging.info("GENERATING GRID")
        coo_max = (max(map(lambda x: max([i[0] for i in x]), self.rock)),
                   max(map(lambda x: max([i[1] for i in x]), self.rock)))
        coo_min = (min(map(lambda x: min([i[0] for i in x]), self.rock)),
                   0)
        logging.info(f'from {coo_min} to {coo_max}')
        grid = numpy.full(shape=(coo_max[1] + 1, coo_max[0] - coo_min[0] + 1),
                          fill_value=self.EMPTY, dtype=int, order='C')
        for line in self.rock:
            for point_0, point_1 in zip(line[:-1], line[1:]):
                x_0 = point_0[1] - coo_min[1]
                y_0 = point_0[0] - coo_min[0]
                x_1 = point_1[1] - coo_min[1]
                y_1 = point_1[0] - coo_min[0]
                if x_0 == x_1:
                    for y in range(min(y_0, y_1), max(y_0, y_1) + 1):
                        grid[x_0, y] = self.WALL
                if y_0 == y_1:
                    for x in range(min(x_0, x_1), max(x_0, x_1) + 1):
                        grid[x, y_0] = self.WALL
        grid[0, 500 - coo_min[0]] = self.SOURCE
        return grid

    def size_of_grid(self):
        return {'width': self.initial_grid.shape[0],
                'height': self.initial_grid.shape[1]}


myRegolith = Regolith()

def regolith_get_size():
    return myRegolith.size_of_grid()

def get_initial_grid():
    grid_data = myRegolith.initial_grid.tolist()
    return grid_data
