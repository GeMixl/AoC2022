###############################################################
# Advent of Code 2022                                         #
# Day 06 https://adventofcode.com/2021/day/06                 #
# Puzzle input at https://adventofcode.com/2022/day/06/input  #
###############################################################


from collections import deque


def read_input(filename: str) -> []:
    with open(filename, "r") as fs:
        input = fs.read()
    return input


def find_marker(buf):
    return len(set(buf)) == len(buf)


def solve(input, N):
    datastream_buffer = deque(input)
    evaluation_buffer = deque()
    for _ in range(N):
        evaluation_buffer.append(datastream_buffer.popleft())
    idx = N
    while len(evaluation_buffer) >= N and not find_marker(evaluation_buffer):
        evaluation_buffer.popleft()
        evaluation_buffer.append(datastream_buffer.popleft())
        idx += 1
    return(idx)


if __name__ == "__main__":
    filename = "input_day06.txt"
    print("--- Part One ---")
    print(solve(read_input(filename), 4))
    print("--- Part Two ---")
    print(solve(read_input(filename), 14))
    
