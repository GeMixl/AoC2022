###############################################################
# Advent of Code 2022                                         #
# Day 14 https://adventofcode.com/2021/day/14                 #
# Puzzle input at https://adventofcode.com/2022/day/14/input  #
###############################################################

"""
https://topaz.github.io/paste/#XQAAAQAdAwAAAAAAAAA5GEohOB7hGMHs0wiIXZE/X7C0xKOgsHr8JZg/tnnjd/WJizPUjjLFULyxC9DkTpQzaaXUGOWjM0zKzASVW0ew5m1nl6Bgr4ak3fwxUB3qRDKgHw8OMo5djWx/3vrv9Ecvyieu71kwrhZs8EooOgjBWmLho+lVAsIzccSj+z6+QNjhP+rvAWWxZAszImMxud3eP5W8QEqaH2LwvnNS928Duy9VCuqYBfylITDvinA7WQ7H16p86suQxAzE8iWbHg+7JMogg0YFX2ZlPRlRgLIZRfTCsiFKoPZsaXZMSoZ8Nlns+Z9lkOCW2IoALQW5C/RO/47pByG2uZjVBKYrDcBYPmsGi72Itma5GTy9Vt9mc1yfDqoevLbYWlVTcg929VLBo4NcXQYwfmk18BvChXUirBJpUHEDLAzEIPGOb2RUWW9E4EhIzdZIFD2Lqv+LA9LbEzMHCrzRoRdE8fNh2gPBK2RPxkCSWHDj5XGI3sTyHZCLqJIZNhJk1rZIBZbfGCL7zB+e7F3w6KhzKPfDxdmo47omKxn1wkr1LIcL0MGv1Cn/991FiQ==
"""

import logging

logging.basicConfig(level=logging.INFO)

blocked = set()

range_sorted = lambda *p: range(min(p), max(p) + 1)

for ps in [[*map(eval, line.split('->'))] for line in open("input_day14.txt")]:
    for (x1, y1), (x2, y2) in zip(ps, ps[1:]):
        blocked |= {complex(x, y) for x in range_sorted(x1, x2)
                    for y in range_sorted(y1, y2)}

floor = max(x.imag for x in blocked)


def solve_part_i_and_ii(check, path=[500], rock=len(blocked)):
    while True:
        pos = path[-1]
        for dest in pos + 1j, pos - 1 + 1j, pos + 1 + 1j:
            if dest not in blocked and dest.imag < floor + 2:
                path.append(dest)
                break
        else:
            if check(pos): return len(blocked) - rock
            blocked.add(pos)
            del path[-1]


if __name__ == "__main__":
    filename = "test_day14.txt"
    print("--- Part One ---")
    print(solve_part_i_and_ii(lambda pos: pos.imag > floor))
    print("--- Part Two ---")
    print(solve_part_i_and_ii(lambda pos: pos == 500) +1)

