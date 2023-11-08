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

def render_screen(scn):
    lines = ["".join(scn[i:i+40]) for i in range(0, len(scn)-1, 40)]
    return "\n".join(lines)

def solve_part_i(input):
    cycles = np.cumsum(np.array([i[2] for i in input]))
    strength = 1 + np.cumsum(np.array([i[1] for i in input]))
    evaluation_intervals = [i for i in range(20, cycles[-1], 40)]
    cycle_intervals = np.searchsorted(cycles, evaluation_intervals, side='left') - 1
    return sum(strength[cycle_intervals] * evaluation_intervals)

def solve_part_ii(input):
    screen = ["."] * sum([i[2] for i in input])
    pixel_position = 0
    sprite_offset = 0
    sprite_position = 1
    for _, jmp, cyc in input:
        for cycle in range(cyc):
            if sprite_offset + sprite_position - 1 == pixel_position:
                screen[pixel_position] = "#"
            if sprite_offset + sprite_position == pixel_position:
                screen[pixel_position] = "#"
            if sprite_offset + sprite_position + 1 == pixel_position:
                screen[pixel_position] = "#"
            pixel_position += 1
        sprite_position += jmp
        sprite_offset = 40 * (pixel_position//40)
    return render_screen(screen)

if __name__ == "__main__":
    filename = "input_day10.txt"
    print("--- Part One ---")
    print(solve_part_i(read_input(filename)))
    print("--- Part Two ---")
    print(solve_part_ii(read_input(filename)))
    
