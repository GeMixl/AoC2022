###############################################################
# Advent of Code 2021                                         #
# Day 05 https://adventofcode.com/2021/day/05                 #
# Puzzle input at https://adventofcode.com/2022/day/05/input  #
###############################################################


import parse
from itertools import zip_longest
from collections import deque


def read_input(filename: str) -> []:
    with open(filename, "r") as fs:
        (block_1, block_2) = fs.read().split("\n\n")
    stack_index = block_1.split("\n")[-1][1::4]
    stack_columns = [[None if i == ' ' else i for i in line[1::4]] for line in block_1.split("\n")[-2::-1]]
    stack_rows = list(map(list, zip_longest(*stack_columns, fillvalue=None)))
    stack = {int(k): [i for i in v if i is not None] for k, v in zip(stack_index, stack_rows)}
    instructions = [parse.parse("move {n_crates:d} from {from:d} to {to:d}", line).named for line in block_2.split("\n")]
    return (stack, instructions)

# [Z] [M] [P]
# 0123456789
#  ^   ^   ^

def print_stack(stack):
    stack_rows = [col for _, col in stack.items()]
    stack_cols = list(map(list, zip_longest(*stack_rows, fillvalue=' ')))
    for cols in stack_cols[::-1]:
        print(cols)
    print()

def solve_part_i(input):
    stack, instructions = input
    stack = {k: deque(v) for k, v in stack.items()}
    for instruction in instructions:
        for _ in range(instruction['n_crates']):
            stack[instruction['to']].append(stack[instruction['from']].pop())
    return "".join(crate[-1] for _, crate in stack.items())

def solve_part_ii(input):
    stack, instructions = input
    stack = {k: deque(v) for k, v in stack.items()}
    print_stack(stack)
    for instruction in instructions:
        transit_stack = []
        for _ in range(instruction['n_crates']):
            transit_stack += stack[instruction['from']].pop()
        stack[instruction['to']] += transit_stack[::-1]
        print_stack(stack)
    return "".join(crate[-1] for _, crate in stack.items())


if __name__ == "__main__":
    filename = "input_day05.txt"
    print("--- Part One ---")
    print(solve_part_i(read_input(filename)))
    print("--- Part Two ---")
    print(solve_part_ii(read_input(filename)))
    
