###############################################################
# Advent of Code 2022                                         #
# Day 13 https://adventofcode.com/2021/day/13                 #
# Puzzle input at https://adventofcode.com/2022/day/13/input  #
###############################################################

from itertools import zip_longest
import pytest


def test_compare_pairs_i():
    left_side = [1,1,3,1,1]
    right_side = [1,1,5,1,1]
    assert compare_pair(left_side, right_side) == True


def test_compare_pairs_ii():
    left_side = [1,1,3,1,1]
    right_side = [1,1,2,1,1]
    assert compare_pair(left_side, right_side) == False


def test_compare_pairs_iii():
    left_side = [[1],[2,3,4]]
    right_side = [[1],4]
    assert compare_pair(left_side, right_side) == True


def test_compare_pairs_iv():
    left_side = [9]
    right_side = [[8,7,6]]
    assert compare_pair(left_side, right_side) == False


def test_compare_pairs_v():
    left_side = [[4,4],4,4]
    right_side = [[4,4],4,4,4]
    assert compare_pair(left_side, right_side) == True


def test_compare_pairs_vi():
    left_side = [7,7,7,7]
    right_side = [7,7,7]
    assert compare_pair(left_side, right_side) == False


def test_compare_pairs_vii():
    left_side = []
    right_side = [3]
    assert compare_pair(left_side, right_side) == True


def test_compare_pairs_viii():
    left_side = [[[]]]
    right_side = [[]]
    assert compare_pair(left_side, right_side) == False


def test_compare_pairs_ix():
    left_side = [1,[2,[3,[4,[5,6,7]]]],8,9]
    right_side = [1,[2,[3,[4,[5,6,0]]]],8,9]
    assert compare_pair(left_side, right_side) == False


def read_input(filename: str) -> []:
    with open(filename, "r") as fs:
        input = [[line.strip() for line in pair.split('\n')] for pair in fs.read().split('\n\n')]
    return input


def compare_pair(left_side, right_side):
    for l, r in zip_longest(left_side, right_side, fillvalue=None):
        res = None
        if isinstance(l, int) and isinstance(r, int):
            if l == r:
                continue
            else:
                return l < r
        elif isinstance(l, list) and isinstance(r, list):
            res =  compare_pair(l, r)
        elif isinstance(l, int) and isinstance(r, list):
            res = compare_pair([l], r)
        if isinstance(l, list) and isinstance(r, int):
            res = compare_pair(l, [r])
        if l is None:
            return True
        if r is None:
            return False
        if res is not None: return res


def solve_part_i(input):
    return sum([i+1 for i in range(len(input)) if compare_pair(eval(input[i][0]), eval(input[i][1]))])


def solve_part_ii(input):
    print(input)
    flattened = [i for item in input for i in item]
    print(['[[6]]']+ ['[[2]]'] + flattened)
    flattened.sort(key=compare_pair)
    print(flattened)


if __name__ == "__main__":
    filename = "test_day13.txt"
    print("--- Part One ---")
    print(solve_part_i(read_input(filename)))
    print("--- Part Two ---")
    print(solve_part_ii(read_input(filename)))
    
