###############################################################
# Advent of Code 2022                                         #
# Day 09 https://adventofcode.com/2021/day/09                 #
# Puzzle input at https://adventofcode.com/2022/day/09/input  #
###############################################################


import numpy as np


moves = {(-1, 0):
             {(1, 0): (1, 0),
              (1, 1): (1, 1),
              (1, -1): (1, -1)
              },
         (-1, 1):
             {(-1, -1): (0, -1),
              (0, -1): (1, -1),
              (1, -1): (1, -1),
              (1, 0): (1, -1),
              (1, 1): (1, 0)
              }

         }

def read_input(filename: str) -> []:
    with open(filename, "r") as fs:
        input = [(line.strip().split(" ")[0], int(line.strip().split(" ")[1])) for line in fs]
    return input


def move_tail(head_pos_init, head_pos_prox, tail_pos_init):
    rel_tail_position = (tail_pos_init[0] - head_pos_init[0], tail_pos_init[1] - head_pos_init[1])
    rel_head_movement = (head_pos_prox[0] - head_pos_init[0], head_pos_prox[1] - head_pos_init[1])
    move_table = {}
    for a, b, c, d in [(1, 0, 0, 1), (0, 1, -1, 0), (-1, 0, 0, -1), (0, -1, 1, 0)]:
        for x, y in moves.keys():
            move_table[(a*x + b*y, c*x + d*y)] = {(a*i + b*j, c*i + d*j): (a*m + b*n, c*m + d*n)
                                                  for (i, j), (m, n) in moves[(x, y)].items()
                                                  }
    if rel_tail_position in move_table.keys():
        if rel_head_movement in move_table[rel_tail_position].keys():
            return tail_pos_init[0] + move_table[rel_tail_position][rel_head_movement][0], tail_pos_init[1] + move_table[rel_tail_position][rel_head_movement][1]
        else:
            return tail_pos_init
    else:
        return tail_pos_init

def move_head(ini_head_position, move):
    if move == 'D':
        return ini_head_position[0] - 1, ini_head_position[1]
    if move == 'U':
        return ini_head_position[0] + 1, ini_head_position[1]
    if move == 'R':
        return ini_head_position[0], ini_head_position[1] + 1
    if move == 'L':
        return ini_head_position[0], ini_head_position[1] - 1

def solve_part_i(input):
    path_length = sum((l[1] for l in input))
    head_positions = [(0, 0)]*(path_length+1)
    tail_positions = [(0, 0)]*(path_length+1)
    idx = 0
    for m, d in input:
        for _ in range(d):
            head_positions[idx+1] = move_head(head_positions[idx], m)
            tail_positions[idx+1] = move_tail(head_positions[idx], head_positions[idx+1], tail_positions[idx])
            idx += 1
    result_set = set(tail_positions)

    return len(result_set)

def solve_part_ii(input):
    path_length = sum((l[1] for l in input))
    head_positions = [(0, 0)]*(path_length+1)
    tail_positions = [(0, 0)]*(path_length+1)
    idx = 0
    for m, d in input:
        for _ in range(d):
            head_positions[idx+1] = move_head(head_positions[idx], m)
            tail_positions[idx+1] = move_tail(head_positions[idx], head_positions[idx+1], tail_positions[idx])
            print(f'head {head_positions[idx]} --> {head_positions[idx+1]}, tail follows {tail_positions[idx]} --> {tail_positions[idx+1]}')
            idx += 1
    result_set = set(tail_positions)

    return len(result_set)

if __name__ == "__main__":
    filename = "input_day09.txt"
    print("--- Part One ---")
    print(solve_part_i(read_input(filename)))
    print("--- Part Two ---")
    print(solve_part_ii(read_input(filename)))
    
