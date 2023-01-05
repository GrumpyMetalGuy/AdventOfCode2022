import sys
from copy import deepcopy
from typing import Set, Dict

from aoc.utils import read_inputs

sys.setrecursionlimit(2500)


def _dfs(cavern, location, max_x, max_y, max_z, visited: Set, cache: Dict) -> bool:
    if location in cache:
        return cache[location]

    if (
        location[0] <= 0
        or location[0] == max_x
        or location[1] <= 0
        or location[1] == max_y
        or location[2] <= 0
        or location[2] == max_z
    ):
        cache[location] = True
        return True

    if cavern[location[0]][location[1]][location[2]]:
        cache[location] = False
        return False

    visited_copy = deepcopy(visited)

    visited_copy.add(location)

    for x_offset, y_offset, z_offset in [
        (-1, 0, 0),
        (1, 0, 0),
        (0, -1, 0),
        (0, 1, 0),
        (0, 0, -1),
        (0, 0, 1),
    ]:
        next_location = (
            location[0] + x_offset,
            location[1] + y_offset,
            location[2] + z_offset,
        )

        if next_location not in visited_copy:
            sub_visited_copy = deepcopy(visited_copy)

            result = _dfs(
                cavern, next_location, max_x, max_y, max_z, sub_visited_copy, cache
            )

            if result:
                cache[location] = True
                return True

    cache[location] = False
    return False


def count_drops(drops, exclude_internal) -> int:
    max_x = max_y = max_z = -1

    for location in drops:
        max_x = max(max_x, location[0])
        max_y = max(max_y, location[1])
        max_z = max(max_z, location[2])

    max_x += 2
    max_y += 2
    max_z += 2

    cavern = []

    for x in range(0, max_x):
        new_x_row = []

        for y in range(0, max_y):
            new_y_row = []

            for z in range(0, max_z):
                new_y_row.append(False)

            new_x_row.append(new_y_row)

        cavern.append(new_x_row)

    for location in drops:
        cavern[location[0]][location[1]][location[2]] = True

    exposed_count = 0

    dfs_cache = {}

    for x in range(0, max_x):
        for y in range(0, max_y):
            for z in range(0, max_z):
                if cavern[x][y][z]:
                    for x_offset, y_offset, z_offset in [
                        (-1, 0, 0),
                        (1, 0, 0),
                        (0, -1, 0),
                        (0, 1, 0),
                        (0, 0, -1),
                        (0, 0, 1),
                    ]:
                        if not cavern[x + x_offset][y + y_offset][z + z_offset]:
                            if not exclude_internal:
                                exposed_count += 1
                            else:
                                can_reach_edge = _dfs(
                                    cavern,
                                    (x + x_offset, y + y_offset, z + z_offset),
                                    max_x,
                                    max_y,
                                    max_z,
                                    set(),
                                    dfs_cache,
                                )

                                if can_reach_edge:
                                    exposed_count += 1

    return exposed_count


def main():
    lava_drops = read_inputs(18, False)

    lava_drops = list(map(eval, lava_drops))

    part_a = count_drops(lava_drops, False)

    print(part_a)

    part_b = count_drops(lava_drops, True)

    print(part_b)
