###############################################################
# Advent of Code 2022                                         #
# Day 15 https://adventofcode.com/2021/day/15                 #
# Puzzle input at https://adventofcode.com/2022/day/15/input  #
###############################################################

from parse import parse
from sys import maxsize

"""
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
...
"""

def read_input(filename: str) -> []:
    with open(filename, "r") as fs:
        input = [parse("Sensor at x={x:d}, y={y:d}: closest beacon is at x={b_x:d}, y={b_y:d}", line.strip()).named
                 for line in fs]
    return input


def get_manhattan_distance(s_x, s_y, d_x, d_y):
    delta_x = abs(d_x - s_x)
    delta_y = abs(d_y - s_y)
    return delta_x + delta_y

def get_cells_with_beacons(l, beacon_positions):
    return sum(1 for p in beacon_positions if (p[1] == l))


def solve_part_i(input, l):
    line_y = l
    cells_with_beacons = len(set([(p['b_x'], p['b_y']) for p in input if p['b_y'] == l]))
    range = []
    manhattan_distances = [get_manhattan_distance(sensor['x'], sensor['y'], sensor['b_x'], sensor['b_y'])
                           for sensor in input]
    for sensor, manhattan_distance in zip(input, manhattan_distances):
        delta_y = abs(line_y - sensor['y']) + 1
        if delta_y <= manhattan_distance + 1:
            remaining_distance = manhattan_distance - delta_y + 1
            range.append((sensor["x"]-remaining_distance, sensor["x"]+remaining_distance))
            # From https://www.geeksforgeeks.org/python-custom-sorting-in-list-of-tuples/
            range = sorted(range, key = lambda sub: (sub[0], -sub[1]))
    covered_cells = 0
    end_of_range = -maxsize
    for r in range:
        # ranges do not overlap
        if (end_of_range < r[0]):
            covered_cells += (r[1] - r[0] + 1)
            end_of_range = r[1]
        # ranges overlap and previous range does not include the active range:
        if (end_of_range >= r[0]) & (end_of_range < r[1]):
            covered_cells += (r[1] - end_of_range)
            end_of_range = r[1]
    return covered_cells - cells_with_beacons

def solve_part_ii(input, search_area):
    min_x, max_x = search_area
    min_y, max_y = search_area
    manhattan_distances = [get_manhattan_distance(sensor['x'], sensor['y'], sensor['b_x'], sensor['b_y'])
                           for sensor in input]
    sensor_distances = [min_y - sensor['y'] for sensor in input]
    sensor_positions = [sensor['x'] for sensor in input]
    beacon_positions = set([(sensor['b_x'], sensor['b_y']) for sensor in input])
    free_cells = set()
    for line in range(min_y, max_y + 1):
        ranges = []
        for position, distance, manhattan_distance in zip(sensor_positions, sensor_distances, manhattan_distances):
            if abs(distance) <= manhattan_distance:
                remaining_distance = manhattan_distance - abs(distance)
                ranges.append((position-remaining_distance, position+remaining_distance))
                # From https://www.geeksforgeeks.org/python-custom-sorting-in-list-of-tuples/
        sensor_distances = [d+1 for d in sensor_distances]
        first_free_cell = min_x
        for occupied in sorted(ranges, key = lambda sub: (sub[0], -sub[1])):
            if first_free_cell < occupied[0] < max_x:
                print(f'Found free range in line {line} between {first_free_cell} and {occupied[0]-1}')
                for column in range(first_free_cell, occupied[0]):
                    free_cells.add((line, column))
            if first_free_cell < occupied[1]:
                first_free_cell = occupied[1] + 1
    return [cell[1] * max_x + cell[0] for cell in free_cells]


if __name__ == "__main__":
    filename = "test_day15.txt"
    filename = "input_day15.txt"
    line_number = 10
    line_number = 2_000_000
    print("--- Part One ---")
    print(solve_part_i(read_input(filename), line_number))
    print("--- Part Two ---")
    print(solve_part_ii(read_input(filename), (0, 4_000_000)))
    
