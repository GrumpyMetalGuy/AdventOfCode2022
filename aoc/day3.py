from aoc.utils import read_inputs
from more_itertools import chunked


def get_priority(value):
    if value.islower():
        return 1 + ord(value) - ord("a")
    else:
        return 27 + ord(value) - ord("A")


def main():
    contents = read_inputs(3, False)

    part_a = 0
    part_b = 0

    for rucksack in contents:
        first_compartment = set(rucksack[: len(rucksack) // 2])
        second_compartment = set(rucksack[len(rucksack) // 2 :])

        common = first_compartment.intersection(second_compartment).pop()

        part_a = part_a + get_priority(common)

    for first, second, third in chunked(contents, 3):
        common = set(first).intersection(set(second)).intersection(set(third)).pop()
        part_b = part_b + get_priority(common)

    print(f"Part A: {part_a}")
    print(f"Part B: {part_b}")
