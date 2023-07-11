from functools import reduce


def read_input(filename: str) -> []:
    with open(filename, "r") as fs:
        input = [[int(food) for food in elf.split("\n")] for elf in fs.read().split("\n\n")]
    return input


def get_calories_for_each_elf(food_list: []) ->  []:
    return [reduce(lambda a, b: a + b, items) for items in food_list]


def solve_part_i(input: []) -> int:
    calories = get_calories_for_each_elf(input)
    return max(calories)


def solve_part_ii(input: []) -> int:
    calories = get_calories_for_each_elf(input)
    return sum((sorted(calories)[-3:]))


if __name__ == "__main__":

    filename = "input_day01.txt"

    print("--- Part One ---")
    print(solve_part_i(read_input(filename)))
    print("--- Part Two ---")
    print(solve_part_ii(read_input(filename)))