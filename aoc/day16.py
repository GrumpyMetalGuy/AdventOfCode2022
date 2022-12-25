import re
from typing import Dict, Set, Tuple, Optional

from aoc.utils import read_inputs
from itertools import product
from collections import namedtuple, defaultdict

Valve = namedtuple("Valve", ["flow", "neighbours"])


def _dfs_impl(
    network: Dict[str, Valve], current: str, end: str, total: int, visited: Set[str]
):
    if current == end:
        return total

    visited = visited.copy()
    visited.add(current)

    next_nodes = (set(network.keys()) - visited).intersection(
        network[current].neighbours
    )

    if not next_nodes:
        return None

    results = list(
        filter(
            None,
            [
                _dfs_impl(network, next_node, end, total + 1, visited)
                for next_node in next_nodes
            ],
        )
    )

    if results:
        return min(results)
    else:
        return None


def dfs(network: Dict[str, Valve], start: str) -> Dict[Tuple[str, str], int]:
    target_nodes = [node for node, valve in network.items() if valve.flow != 0] + [
        start
    ]

    possible_pairs = product(target_nodes, target_nodes)

    costs = dict()

    for start, finish in possible_pairs:
        if start == finish:
            continue

        costs[(start, finish)] = _dfs_impl(network, start, finish, 0, set())

    return costs


class Network:
    def __init__(
        self, network: Dict[str, Valve], start: str, time: int, agent_count: int
    ):
        self.network: Dict[str, Valve] = network
        self.start = start
        self.time = time
        self.flowing_valve_locations = set(
            [location for location, valve in network.items() if valve.flow != 0]
        )
        self.costs = dfs(network, start)
        self.agent_count = agent_count

    def _dfs(self, current, remaining, visited, total, history) -> Optional[int]:
        if remaining < 1:
            return None

        results = []

        for neighbour in self.flowing_valve_locations:
            if neighbour in visited:
                continue

            sub_visited = visited.copy()
            sub_visited.add(neighbour)

            travel_time = self.costs[(current, neighbour)]
            remaining_time = remaining - travel_time - 1

            released = total + remaining_time * self.network[neighbour].flow

            history[tuple(sorted(sub_visited))].append(released)

            neighbour_result = self._dfs(
                neighbour, remaining_time, sub_visited, released, history
            )

            if neighbour_result is not None:
                results.append(released + neighbour_result)
            else:
                results.append(released)

        results = list(filter(None, results))

        if results:
            return max(results)
        else:
            return None

    def calculate_new(self) -> int:
        history = defaultdict(list)

        self._dfs("AA", self.time, set(), 0, history)

        released = -99999

        if self.agent_count == 1:
            for values in history.values():
                released = max(released, max(values))

            return released

        for history_entry, history_values in history.items():
            for other_history_entry, other_history_values in history.items():
                if history_entry == other_history_entry:
                    continue

                if not set(history_entry).intersection(set(other_history_entry)):
                    released_pressure = max(history_values) + max(other_history_values)

                    released = max(released, released_pressure)

        return released


def main():
    valve_descriptions = read_inputs(16, False)

    valve_re = re.compile(
        r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
    )

    valves = {}

    for valve_description in valve_descriptions:
        valve, flow, neighbours = re.findall(valve_re, valve_description)[0]

        valves[valve] = Valve(
            int(flow), [neighbour.strip() for neighbour in neighbours.split(",")]
        )

    network = Network(valves, "AA", 30, 1)
    part_a = network.calculate_new()

    print(f"Part A: {part_a}")

    network = Network(valves, "AA", 26, 2)
    part_b = network.calculate_new()
    print(f"Part B: {part_b}")
