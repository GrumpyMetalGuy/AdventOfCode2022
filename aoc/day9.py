from typing import List

from aoc.utils import read_inputs


def simulate(rope_directions: List[str], knot_count: int) -> int:
    knots = []

    for knot_counter in range(0, knot_count):
        knots.append([0, 0])

    visited = {(0, 0)}

    for rope_direction in rope_directions:
        direction, length = rope_direction.split(" ")

        length = int(length)

        for counter in range(0, length):
            if direction == "R":
                knots[0][0] += 1
            elif direction == "L":
                knots[0][0] -= 1
            elif direction == "U":
                knots[0][1] += 1
            else:
                knots[0][1] -= 1

            for first, second in zip(knots[0:-1], knots[1:]):
                tail_location_diff = [first[0] - second[0], first[1] - second[1]]

                if tail_location_diff[0] in [-1, 0, 1] and tail_location_diff[1] in [
                    -1,
                    0,
                    1,
                ]:
                    continue

                if tail_location_diff[0] != 0:
                    second[0] += int(tail_location_diff[0] / abs(tail_location_diff[0]))

                if tail_location_diff[1] != 0:
                    second[1] += int(tail_location_diff[1] / abs(tail_location_diff[1]))

            visited.add(tuple(knots[-1]))

    return len(visited)


def main():
    rope_directions = read_inputs(9, False)

    print(f"Part A: {simulate(rope_directions, 2)}")
    print(f"Part B: {simulate(rope_directions, 10)}")
