###############################################################
# Advent of Code 2021                                         #
# Day 03 https://adventofcode.com/2021/day/03                 #
# Puzzle input at https://adventofcode.com/2022/day/03/input  #
###############################################################
from collections import deque
from string import ascii_lowercase, ascii_uppercase


def read_input(filename: str) -> []:
    with open(filename, "r") as fs:
        input = [line.strip() for line in fs]
    return input


def split_line(line: str) -> []:
    first_part = line[:len(line)//2]
    second_part = line[len(line)//2:]
    return([first_part, second_part])


def find_double_item(cmp: []) -> str:
    return next(i for i in cmp[0] if i in cmp[1])


def get_item_value(item: str) -> int:
    values = ascii_lowercase + ascii_uppercase
    return next(i+1 for i, letter in enumerate(values) if letter == item)


def solve_part_i(input):
    compartments = [split_line(i) for i in input]
    value = 0
    for c in compartments:
        item = find_double_item(c)
        value += get_item_value(item)
    return(value)


def solve_part_ii(input):
    elf_queue = deque(input)
    sticker_attachment_effort = 0
    while len(elf_queue) > 0:
        current_elf = elf_queue.popleft()
        other_elfs = [elf_queue.popleft(), elf_queue.popleft()]
        for i in "".join(set(current_elf)):
            badge = [elf for elf in other_elfs if i in elf]
            if len(badge) == 2:
                sticker_attachment_effort += get_item_value(i)
    return sticker_attachment_effort


if __name__ == "__main__":
    filename = "input_day03.txt"
    print("--- Part One ---")
    print(solve_part_i(read_input(filename)))
    print("--- Part Two ---")
    print(solve_part_ii(read_input(filename)))
    
