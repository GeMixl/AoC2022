###############################################################
# Advent of Code 2021                                         #
# Day 02 https://adventofcode.com/2021/day/02                 #
# Puzzle input at https://adventofcode.com/2022/day/02/input  #
###############################################################


from itertools import product, cycle, islice, chain


def read_input(filename: str) -> []:
    with open(filename, "r") as fs:
        input = [line.strip() for line in fs]
    return input


def solve_part_i(input):
    """
       A X -> 3 + 1
       A Y -> 6 + 1
       A Z -> 0 + 1
       (3, 6, 0) + 1

       B X -> 0 + 2
       B Y -> 3 + 2
       ...
       (0, 3, 6) + 2

       C X -> 6 + 3
       ...
       (6, 0, 3) + 3
       """
    draw_win_loose = [3, 6, 0]
    games = [i + " " + j for i, j in product("ABC", "XYZ")]
    points = chain.from_iterable(
        [list(islice(cycle(draw_win_loose), 2 * i, 2 * i + 3, 1))
         for i in range(len(draw_win_loose))]
    )
    game_score = {k: v for k, v in zip(games, points)}
    extra_score = {k: v for k, v in zip(games, cycle((1, 2, 3)))}

    strategy_guide = input
    total_score = [game_score[game] + extra_score[game] for game in strategy_guide]
    return sum(total_score)


def solve_part_ii(input):
    """
       A X -> R -- S -> 0 + 3
       A Y -> R -- R -> 3 + 1
       A Z -> R -- P -> 6 + 2
       (0, 3, 6) + (3, 1, 2)

       B X -> P -- R: 0 + 1
       B Y -> P -- P: 3 + 2
       B Z -> P -- S: 6 + 3
       ...
       (0, 3, 6) + (1, 2, 3)

       C X -> S -- P: 0 + 2
       ...
       (0, 3, 6) + (2, 3, 1)
       """
    games = [i + " " + j for i, j in product("ABC", "XYZ")]
    game_score = {k: v for k, v in zip(games, cycle((0, 3, 6)))}
    rock_paper_scissors = [1, 2, 3]
    extra_points = chain.from_iterable(
        [list(islice(cycle(rock_paper_scissors), i+2, i+5))
         for i in range(len(rock_paper_scissors))]
    )
    extra_score = {k: v for k, v in zip(games, extra_points)}
    strategy_guide = input

    total_score = [game_score[game] + extra_score[game] for game in strategy_guide]
    return sum(total_score)

if __name__ == "__main__":
    filename = "test_day02.txt"
    filename = "input_day02.txt"


    print("--- Part One ---")
    print(solve_part_i(read_input(filename)))
    print("--- Part Two ---")
    print(solve_part_ii(read_input(filename)))
    
