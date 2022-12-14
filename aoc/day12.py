from collections import deque, namedtuple
from typing import List

from aoc.utils import read_inputs

Node = namedtuple("Node", ["coords", "distance"])


def search(heightmap: List[List[str]], start: Node, end: Node) -> int:
    queue = deque([start])

    visited = {start.coords}

    while queue:
        current_node = queue.popleft()
        current_node_height = heightmap[current_node.coords[0]][current_node.coords[1]]

        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            current_line = current_node.coords[0] + offset[0]
            current_col = current_node.coords[1] + offset[1]

            if not (
                0 <= current_line < len(heightmap)
                and 0 <= current_col < len(heightmap[1])
            ):
                continue

            next_node_coords = (current_line, current_col)
            next_node_height = heightmap[next_node_coords[0]][next_node_coords[1]]

            if current_node_height in ["y", "z"] and next_node_coords == end.coords:
                return current_node.distance + 1

            if next_node_coords in visited:
                continue

            if ord(next_node_height) - ord(current_node_height) <= 1:
                queue.append(Node(next_node_coords, current_node.distance + 1))
                visited.add(next_node_coords)

    return end.distance


def main():
    heightmap_inputs = read_inputs(12, False)

    heightmap = [list(heightmap_input) for heightmap_input in heightmap_inputs]

    start = None
    end = None

    lowest_starting_points = []

    for heightmap_line, heightmap_cols in enumerate(heightmap):
        for heightmap_col, heightmap_value in enumerate(heightmap_cols):
            if heightmap_value == "E":
                end = Node((heightmap_line, heightmap_col), 0)
            elif heightmap_value == "S":
                start = Node((heightmap_line, heightmap_col), 0)
                heightmap[heightmap_line][heightmap_col] = "a"
                lowest_starting_points.append(Node((heightmap_line, heightmap_col), 0))
            elif heightmap_value == "a":
                lowest_starting_points.append(Node((heightmap_line, heightmap_col), 0))

    part_a = search(heightmap, start, end)

    print(f"Part A: {part_a}")

    part_b = 9999999

    for start in lowest_starting_points:
        result = search(heightmap, start, end)

        if result:
            part_b = min(part_b, result)

    print(f"Part B: {part_b}")
