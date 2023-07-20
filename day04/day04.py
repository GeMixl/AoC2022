###############################################################
# Advent of Code 2021                                         #
# Day 04 https://adventofcode.com/2021/day/04                 #
# Puzzle input at https://adventofcode.com/2022/day/04/input  #
###############################################################


def read_input(filename: str) -> []:
    with open(filename, "r") as fs:
        input = [[[int(limit) for limit in range.strip().split('-')] for range in line.split(",")] for line in fs]
    return input


def solve_part_i(input):
    result = [(range_2[0] <= range_1[0] <= range_2[1] and
               range_2[0] <= range_1[1] <= range_2[1]) or
              (range_1[0] <= range_2[0] <= range_1[1] and
               range_1[0] <= range_2[1] <= range_1[1])
              for (range_1, range_2) in input]
    return sum(result)



def solve_part_ii(input):
    result = [range_2[0] <= range_1[0] <= range_2[1] or
              range_2[0] <= range_1[1] <= range_2[1] or
              range_1[0] <= range_2[0] <= range_1[1] or
              range_1[0] <= range_2[1] <= range_1[1]
              for (range_1, range_2) in input]
    return sum(result)


if __name__ == "__main__":
    filename = "input_day04.txt"
    print("--- Part One ---")
    print(solve_part_i(read_input(filename)))
    print("--- Part Two ---")
    print(solve_part_ii(read_input(filename)))
    
