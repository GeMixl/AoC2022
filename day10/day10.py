###############################################################
# Advent of Code 2022                                         #
# Day 10 https://adventofcode.com/2021/day/10                 #
# Puzzle input at https://adventofcode.com/2022/day/10/input  #
###############################################################


import numpy as np


def read_input(filename: str) -> []:
    with open(filename, "r") as fs:
        input = [[line.strip(), 0, 1] if line.strip() == 'noop' else [line.split(' ')[0], int(line.split(' ')[1]), 2]
                 for line in fs]
    return input


def solve_part_i(input):
    cycles = np.cumsum(np.array([i[2] for i in input]))
    strength = np.cumsum(np.array([i[1] for i in input])) + 1
    evaluation_intervals = [i for i in range(20, cycles[-1], 40)]
    strength_fluctuations = np.stack((np.array([i for i in range(len(cycles))]), cycles, strength), axis=1)
    print(evaluation_intervals)
    cycle_intervals = np.searchsorted(cycles, evaluation_intervals, side='left')-1
    print(cycle_intervals)
    return sum(strength[cycle_intervals] * evaluation_intervals)

def solve_part_ii(input):
    pass


if __name__ == "__main__":
    filename = "input_day10.txt"
    print("--- Part One ---")
    print(solve_part_i(read_input(filename)))
    print("--- Part Two ---")
    print(solve_part_ii(read_input(filename)))
    
