import operator
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from typing import List

from more_itertools import split_at

from aoc.utils import read_inputs


@dataclass
class Monkey:
    items: List[int] = None
    operation: str = None
    test_divisible: int = None
    test_true: int = None
    test_false: int = None


def process_monkey_shenanigans(
    monkey_shenanigans: List[str], rounds: int, reduce_worry: bool
) -> int:
    monkeys = {}

    for monkey_description in split_at(monkey_shenanigans, lambda desc: not desc):
        monkey_id = int(monkey_description[0].split(" ")[1].strip(" :"))
        items = [
            int(item.strip()) for item in monkey_description[1].split(":")[1].split(",")
        ]
        operation = monkey_description[2].split("=")[1].strip()[4:]
        test_divisible = int(monkey_description[3].split("by ")[1])
        test_true = int(monkey_description[4].split("monkey ")[1])
        test_false = int(monkey_description[5].split("monkey ")[1])

        monkeys[monkey_id] = Monkey(
            items, operation, test_divisible, test_true, test_false
        )

    common_divisor = reduce(
        lambda x, y: x * y, [monkey.test_divisible for monkey in monkeys.values()]
    )

    monkey_counts = defaultdict(int)

    monkey_ids = sorted(monkeys)

    for current_round in range(0, rounds):
        for monkey_id in monkey_ids:
            current_monkey = monkeys[monkey_id]
            worry_operator, orig_value = current_monkey.operation.split(" ")

            value_operator = {"*": operator.mul, "+": operator.add, "-": operator.sub}[
                worry_operator
            ]

            for current_item in current_monkey.items:
                if orig_value == "old":
                    value = current_item
                else:
                    value = int(orig_value)

                current_item = value_operator(current_item, value)

                if reduce_worry:
                    current_item = current_item // 3
                else:
                    current_item = current_item % common_divisor

                if current_item % current_monkey.test_divisible:
                    monkeys[current_monkey.test_false].items.append(current_item)
                else:
                    monkeys[current_monkey.test_true].items.append(current_item)

                monkey_counts[monkey_id] += 1

            current_monkey.items = []

    counts = sorted(monkey_counts.values())

    return counts[-2] * counts[-1]


def main():
    monkey_shenanigans = read_inputs(11, False)

    print(f"Part A: {process_monkey_shenanigans(monkey_shenanigans, 20, True)}")
    print(f"Part B: {process_monkey_shenanigans(monkey_shenanigans, 10000, False)}")
