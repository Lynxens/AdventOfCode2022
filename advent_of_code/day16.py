from typing import Tuple, Dict, List
from abstract_puzzles import AbstractPuzzles
import re
from itertools import combinations

DATA_TYPE = Dict[str, Tuple[int, Dict[str, int]]]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=16,
            puzzle_1_example_answer=1651,
            puzzle_1_answer=1862,
            puzzle_2_example_answer=1707,
            puzzle_2_answer=2422,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        valves = {}

        with open(file_path, 'r') as f:
            for line in f.read().splitlines():
                valve, flow_rate, tunnels = re.match(r"Valve ([A-Z]+) .*=(\d+); .*valves? ([A-Z, ]+)", line).groups()

                valves[valve] = (int(flow_rate), tunnels.split(', '))

        working_valves = [valve for valve, (flow_rate, _) in valves.items() if flow_rate > 0]

        return {
            valve: (valves[valve][0], calculate_costs(valves, valve, [v for v in working_valves if v != valve]))
            for valve in working_valves + ['AA']
        },

    def puzzle_1(self, valves: DATA_TYPE) -> int:
        start_valve = 'AA'
        _, tunnels = valves[start_valve]
        unopened_valves = set(tunnels.keys())

        paths = []
        for v in unopened_valves:
            paths.append(check_path(valves, v, unopened_valves, total_pressure=0, time_remaining=30 - tunnels[v]))

        return max(paths)

    def puzzle_2(self, valves: DATA_TYPE) -> int:
        start_valve = 'AA'
        _, tunnels = valves[start_valve]
        unopened_valves = set(tunnels.keys())

        paths = []
        for v1, v2 in combinations(unopened_valves, 2):
            paths.append(check_path_with_elephant(valves, v1, v2, unopened_valves, total_pressure=0, your_time_remaining=26 - tunnels[v1], elephant_time_remaining=26 - tunnels[v2]))

        return max(paths)


def check_path(valves: DATA_TYPE, valve: str, unopened_valves: set, total_pressure: int, time_remaining: int) -> int:
    if time_remaining <= 1 or len(unopened_valves) == 0:
        return total_pressure

    flow_rate, tunnels = valves[valve]

    new_unopened_valves = unopened_valves.copy()
    new_unopened_valves.remove(valve)
    time_remaining -= 1
    total_pressure += flow_rate * time_remaining

    if len(new_unopened_valves) == 0:
        return total_pressure

    paths = []
    for v in new_unopened_valves:
        paths.append(check_path(valves, v, new_unopened_valves, total_pressure, time_remaining - tunnels[v]))

    return max(paths)


def check_path_with_elephant(valves: DATA_TYPE, your_valve: str, elephant_valve: str, unopened_valves: set, total_pressure: int, your_time_remaining: int, elephant_time_remaining: int) -> int:
    if len(unopened_valves) == 0 or (your_time_remaining <= 1 and elephant_time_remaining <= 1):
        return total_pressure

    your_flow_rate, your_tunnels = valves[your_valve]
    elephant_flow_rate, elephant_tunnels = valves[elephant_valve]

    new_unopened_valves = unopened_valves.copy()

    if your_time_remaining > 1:
        your_time_remaining -= 1
        total_pressure += your_flow_rate * your_time_remaining
        new_unopened_valves.remove(your_valve)
        
        if len(new_unopened_valves) == 0:
            return total_pressure

    if elephant_time_remaining > 1:
        elephant_time_remaining -= 1
        total_pressure += elephant_flow_rate * elephant_time_remaining
        new_unopened_valves.remove(elephant_valve)

        if len(new_unopened_valves) == 0:
            return total_pressure

    paths = []
    if your_time_remaining > 1 and elephant_time_remaining > 1:
        for v1, v2 in combinations(new_unopened_valves, 2):
            paths.append(check_path_with_elephant(
                valves, v1, v2, new_unopened_valves, total_pressure,
                your_time_remaining - your_tunnels[v1],
                elephant_time_remaining - elephant_tunnels[v2]
            ))
            paths.append(check_path_with_elephant(
                valves, v2, v1, new_unopened_valves, total_pressure,
                your_time_remaining - your_tunnels[v2],
                elephant_time_remaining - elephant_tunnels[v1]
            ))
    else:
        return total_pressure

    return max(paths) if len(paths) > 0 else total_pressure


def calculate_costs(valves: Dict[str, Tuple[int, List[str]]], start: str, ends: List[str]) -> Dict[str, int]:
    queue = [start]
    visited = set()
    costs = {}
    step_count = 0

    while len(queue) > 0 and len(ends) > 0:
        step_queue = queue
        queue = []

        while len(step_queue) > 0:
            valve = step_queue.pop()

            _, tunnels = valves[valve]

            for tunnel in tunnels:
                if tunnel in visited:
                    continue

                if tunnel in ends:
                    costs[tunnel] = step_count + 1
                    ends.remove(tunnel)

                queue.append(tunnel)

            visited.add(valve)

        step_count += 1

    return costs
