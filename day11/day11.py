###############################################################
# Advent of Code 2022                                         #
# Day 11 https://adventofcode.com/2021/day/11                 #
# Puzzle input at https://adventofcode.com/2022/day/11/input  #
###############################################################
from typing import Any

from parse import *
import pykka
from collections import deque
import operator
from math import prod
import logging

logging.basicConfig(level=logging.INFO)


class Monkey(pykka.ThreadingActor):
    def __init__(self, monkey_id, initial_items, operation, test_divisor):
        super().__init__()
        self.id = monkey_id
        self.items = deque([int(item) for item in initial_items])
        self.test_divisor = int(test_divisor)
        self.operand_1 = operation[0]
        self.operand_2 = operation[2]
        self.operator_mapping = {'+': operator.add,
                                 '*': operator.mul}
        self.operator_function = self.operator_mapping[operation[1]]
        self.true_monkey = None
        self.false_monkey = None
        self.inspect_count = 0

    def on_receive(self, message: Any) -> Any:
        if message['command'] == 'throw':
            self.items.append(message['item'])
            logging.debug(f'Monkey {self.id}: catching item {message["item"]}')
        elif message['command'] == 'start':
            if 'worry_reduction' in message.keys():
                self.inspect_items_with_worry_reduction(int(message['worry_reduction']))
            elif 'with_supermodulo' in message.keys():
                self.inspect_items_w_o_worry_reduction(int(message['with_supermodulo']))
        return True

    def calculate_new_worry_level(self, worry_level):
        op_1 = worry_level if self.operand_1 == 'old' else int(self.operand_1)
        op_2 = worry_level if self.operand_2 == 'old' else int(self.operand_2)
        return self.operator_function(op_1, op_2)

    def check_worry_level(self, item):
        return item % self.test_divisor == 0

    def inspect_items_with_worry_reduction(self, worry_divisor):
        while len(self.items) > 0:
            self.inspect_count += 1
            current_item = self.items.popleft()
            current_item = self.calculate_new_worry_level(current_item) // worry_divisor
            logging.debug(f'Monkey {self.id}: throwing item {current_item}')
            if self.check_worry_level(current_item):
                self.true_monkey.ask({'command': 'throw', 'item': current_item}, block=True)
            else:
                self.false_monkey.ask({'command': 'throw', 'item': current_item}, block=True)

    def inspect_items_w_o_worry_reduction(self, supermodulo):
        while len(self.items) > 0:
            self.inspect_count += 1
            current_item = self.items.popleft()
            current_item = self.calculate_new_worry_level(current_item % supermodulo)
            logging.debug(f'Monkey {self.id}: throwing item {current_item}')
            if self.check_worry_level(current_item):
                self.true_monkey.ask({'command': 'throw', 'item': current_item}, block=True)
            else:
                self.false_monkey.ask({'command': 'throw', 'item': current_item}, block=True)


def read_input(filename: str) -> []:
    with (open(filename, "r") as fs):
        input_string = fs.read().split("\n\n")
        input_blocks = [block.split('\n') for block in input_string]
    monkey_list = []
    for monkey_line in input_blocks:
        id_line_parsed = parse('Monkey {monkey_id:d}:', monkey_line[0].strip())
        item_line_parsed = parse('Starting items: {item_list}', monkey_line[1].strip())
        operation_line_parsed = parse('Operation: new = {operand_1} {operator} {operand_2}', monkey_line[2].strip())
        test_line_parsed = parse('Test: divisible by {divisor:d}', monkey_line[3].strip())
        true_line_parsed = parse('If true: throw to monkey {true_monkey:d}', monkey_line[4].strip())
        false_line_parsed = parse('If false: throw to monkey {false_monkey:d}', monkey_line[5].strip())
        monkey_dict = (
                id_line_parsed.named |
                item_line_parsed.named |
                operation_line_parsed.named |
                test_line_parsed.named |
                true_line_parsed.named |
                false_line_parsed.named
        )
        monkey_dict['item_list'] = tuple([int(item) for item in monkey_dict['item_list'].split(', ')])
        monkey_list.append(monkey_dict)
    return monkey_list


def solve_part_i(input, worry_divisor, n_rounds):
    myMonkeys = [Monkey.start(item['monkey_id'],
                              item['item_list'],
                              [item['operand_1'], item['operator'], item['operand_2']],
                              item['divisor'])
                 for item in input]

    for item in input:
        myMonkeys[item['monkey_id']].proxy().true_monkey = myMonkeys[item['true_monkey']]
        myMonkeys[item['monkey_id']].proxy().false_monkey = myMonkeys[item['false_monkey']]

    for i in range(n_rounds):
        for monkey in myMonkeys:
            monkey.ask({"command": "start", "worry_reduction": 3}, block=True)

    for monkey in myMonkeys:
        logging.warning(monkey._actor.inspect_count)

    business_levels = sorted([monkey._actor.inspect_count for monkey in myMonkeys])
    for monkey in myMonkeys:
            monkey.stop()

    return business_levels[-1] * business_levels[-2]


def solve_part_ii(input, n_rounds):
    myMonkeys = [Monkey.start(item['monkey_id'],
                              item['item_list'],
                              [item['operand_1'], item['operator'], item['operand_2']],
                              item['divisor'])
                 for item in input]

    supermodulo = prod([int(item['divisor']) for item in input])

    for item in input:
        myMonkeys[item['monkey_id']].proxy().true_monkey = myMonkeys[item['true_monkey']]
        myMonkeys[item['monkey_id']].proxy().false_monkey = myMonkeys[item['false_monkey']]

    for i in range(n_rounds):
        for monkey in myMonkeys:
            monkey.ask({"command": "start", 'with_supermodulo': supermodulo}, block=True)

    for monkey in myMonkeys:
        print(monkey._actor.inspect_count)

    business_levels = sorted([monkey._actor.inspect_count for monkey in myMonkeys])
    for monkey in myMonkeys:
        monkey.stop()

    return business_levels[-1] * business_levels[-2]


if __name__ == "__main__":
    filename = "input_day11.txt"
    print("--- Part One ---")
    print(solve_part_i(read_input(filename), 3, 20))
    print("--- Part Two ---")
    print(solve_part_ii(read_input(filename), 10000))
    
