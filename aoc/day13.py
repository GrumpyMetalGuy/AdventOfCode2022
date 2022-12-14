import functools
from itertools import zip_longest

import more_itertools

from aoc.utils import read_inputs


def compare_pair(pair_first, pair_second) -> int:
    if isinstance(pair_first, int) and isinstance(pair_second, int):
        if pair_first > pair_second:
            return -1
        elif pair_first < pair_second:
            return 1
        else:
            return 0

    if isinstance(pair_first, int):
        pair_first = [pair_first]

    if isinstance(pair_second, int):
        pair_second = [pair_second]

    for first, second in zip_longest(pair_first, pair_second):
        if first is None:
            return 1
        elif second is None:
            return -1

        result = compare_pair(first, second)

        if result != 0:
            return result

    return 0


def main():
    packet_inputs = read_inputs(13, False)

    packet_pairs = list(more_itertools.split_at(packet_inputs, lambda x: not x))

    part_a = 0

    for packet_index, packet_pair in enumerate(packet_pairs):
        result = compare_pair(eval(packet_pair[0]), eval(packet_pair[1]))

        if result == 1:
            part_a += packet_index + 1

    print(f"Part A: {part_a}")

    packet_inputs = [
        eval(packet_input) for packet_input in packet_inputs if packet_input
    ]

    dividers = [[[2]], [[6]]]
    packet_inputs.extend(dividers)

    sorted_packet_inputs = sorted(
        packet_inputs, reverse=True, key=functools.cmp_to_key(compare_pair)
    )

    first_index = sorted_packet_inputs.index(dividers[0]) + 1
    second_index = sorted_packet_inputs.index(dividers[1]) + 1

    print(f"Part B: {first_index * second_index}")
