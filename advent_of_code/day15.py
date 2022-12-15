from typing import Tuple, List
from abstract_puzzles import AbstractPuzzles
import re
import numpy as np

DATA_TYPE = List[Tuple[Tuple[int, int], Tuple[int, int], int]]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=15,
            puzzle_1_example_answer=26,
            puzzle_1_answer=4665948,
            puzzle_2_example_answer=56000011,
            puzzle_2_answer=13543690671045,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        data = []

        with open(file_path, 'r') as f:
            for line in f.read().splitlines():
                sensor_x, sensor_y, beacon_x, beacon_y = tuple(map(
                    int,
                    re.match(r".*x=(-?\d+), y=(-?\d+): .*x=(-?\d+), y=(-?\d+)", line).groups()
                ))

                distance = abs(sensor_y - beacon_y) + abs(sensor_x - beacon_x)
                data.append(((sensor_x, sensor_y), (beacon_x, beacon_y), distance))

        return data,

    def puzzle_1(self, data: DATA_TYPE, highlighted_row: int) -> int:
        sensor_x = np.array([sensor_x for (sensor_x, _), _, _ in data])
        sensor_y = np.array([sensor_y for (_, sensor_y), _, _ in data])
        beacons_in_row = set([beacon_y for _, (_, beacon_y), _ in data if beacon_y == highlighted_row])
        distance = np.array([distance for _, _, distance in data])

        min_x = min(sensor_x)
        max_x = max(sensor_x)
        max_distance = max(distance)

        possible_beacon = np.max(
            np.absolute(np.array([np.arange(min_x - max_distance, max_x + max_distance)] * len(data)).T - sensor_x) + np.absolute(sensor_y - highlighted_row) <= distance,
            axis=1
        )

        return possible_beacon.sum() - len(beacons_in_row)

    def puzzle_2(self, data: DATA_TYPE, upper_bound: int) -> int:
        ranges = [[(0, upper_bound)]] * upper_bound

        for i, ((sensor_x, sensor_y), _, distance) in enumerate(data):
            for y in range(max(sensor_y - distance, 0), min(sensor_y + distance + 1, upper_bound)):
                dy = abs(y - sensor_y)
                row_range = (max(sensor_x - distance + dy, 0), min(sensor_x + distance - dy, upper_bound))
                ranges[y] = self.merge_ranges(ranges[y], row_range)

        for y, r in enumerate(ranges):
            if len(r) > 0:
                return r[0][0] * 4000000 + y

    @staticmethod
    def merge_ranges(ranges: List[Tuple[int, int]], new_range: Tuple[int, int]):
        new_ranges = []
        for (start, end) in ranges:
            if new_range[1] < start or new_range[0] > end:
                new_ranges.append((start, end))
            else:
                if new_range[0] <= start and new_range[1] >= end:
                    continue

                if new_range[0] > start:
                    new_ranges.append((start, new_range[0] - 1))

                if new_range[1] < end:
                    new_ranges.append((new_range[1] + 1, end))

        return new_ranges

    def solve_puzzles(self):
        print(f"Puzzle 1: {self.puzzle_1(*self.data, highlighted_row=2000000)}")
        print(f"Puzzle 2: {self.puzzle_2(*self.data, upper_bound=4000000)}")

    def test_puzzle_1_example(self):
        self.assertEqual(self.puzzle_1_example_answer, self.puzzle_1(*self.data_example, highlighted_row=10))

    def test_puzzle_1(self):
        self.assertEqual(self.puzzle_1_answer, self.puzzle_1(*self.data, highlighted_row=2000000))

    def test_puzzle_2_example(self):
        self.assertEqual(self.puzzle_2_example_answer, self.puzzle_2(*self.data_example, upper_bound=20))

    def test_puzzle_2(self):
        self.assertEqual(self.puzzle_2_answer, self.puzzle_2(*self.data, upper_bound=4000000))
