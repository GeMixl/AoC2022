###############################################################
# Advent of Code 2022                                         #
# Day 08 https://adventofcode.com/2021/day/08                 #
# Puzzle input at https://adventofcode.com/2022/day/08/input  #
###############################################################


import numpy as np


def read_input(filename: str) -> []:
    with open(filename, "r") as fs:
        input = [[int(item) for item in row.strip()] for row in fs]
    return input


def solve_part_i(input):
    forrest = np.array(input)
    nrow, ncol =forrest.shape
    tree_visibility = np.ones_like(forrest, dtype=bool)
    for row in range(1, nrow-1):
        for col in range(1, ncol-1):
#            print(f'Node [{row},{col}]: {forrest[row, col]}: visible from top -> {all(forrest[0:row, col] < forrest[row, col])}')
#            print(f'               visible from bottom -> {all(forrest[row+1:nrow, col] < forrest[row, col])}')
#            print(f'               visible from left -> {all(forrest[row, 0:col] < forrest[row, col])}')
#            print(f'               visible from right -> {all(forrest[row, col+1:ncol] < forrest[row, col])}')
            tree_visibility[row, col] = any([all(forrest[0:row, col] < forrest[row, col]),
                                             all(forrest[row+1:nrow, col] < forrest[row, col]),
                                             all(forrest[row, 0:col] < forrest[row, col]),
                                             all(forrest[row, col+1:ncol] < forrest[row, col])])
    return tree_visibility.sum()


def get_viewing_distance(tree, neighborhood):
    return len(neighborhood) if all(neighborhood < tree) else np.argmax(neighborhood >= tree) + 1


def solve_part_ii(input):
    forrest = np.array(input)
    nrow, ncol = forrest.shape
    scenic_score = np.zeros_like(forrest)
    for row in range(1, nrow-1):
        for col in range(1, ncol-1):
            tree = forrest[row][col]
#            print(f'Node [{row},{col}]: {forrest[row, col]}: neighbors from top -> {get_viewing_distance(forrest[row][col], np.flip(forrest[0:row, col]))}')
#            print(f'               neighbors from bottom -> {get_viewing_distance(forrest[row][col], forrest[row+1:nrow, col])}')
#            print(f'               neighbors from left -> {get_viewing_distance(forrest[row][col], np.flip(forrest[row, 0:col]))}')
#            print(f'               neighbors from right -> {get_viewing_distance(forrest[row][col], forrest[row, col+1:ncol])}')
            scenic_score[row][col] = get_viewing_distance(tree, np.flip(forrest[0:row, col])) * get_viewing_distance(tree, forrest[row+1:nrow, col]) * \
                get_viewing_distance(tree, np.flip(forrest[row, 0:col])) * get_viewing_distance(tree, forrest[row, col+1:ncol])
    print(np.max(scenic_score))



if __name__ == "__main__":
    filename = "input_day08.txt"
    print("--- Part One ---")
    print(solve_part_i(read_input(filename)))
    print("--- Part Two ---")
    print(solve_part_ii(read_input(filename)))
    
