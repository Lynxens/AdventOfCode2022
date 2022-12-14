from typing import Tuple, List
from abstract_puzzles import AbstractPuzzles
import numpy as np

DATA_TYPE = np.ndarray


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=14,
            puzzle_1_example_answer=24,
            puzzle_1_answer=858,
            puzzle_2_example_answer=93,
            puzzle_2_answer=26845,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        lines = []

        with open(file_path, 'r') as f:
            for line in f.read().splitlines():
                coords = line.split(' -> ')

                for i in range(len(coords) - 1):
                    lines.append((
                        tuple(map(int, coords[i].split(','))),
                        tuple(map(int, coords[i + 1].split(','))),
                    ))

        height = max(max(lines, key=lambda x: x[0][1])[0][1], max(lines, key=lambda x: x[1][1])[1][1]) + 3
        width = 1000

        cave = np.zeros((height, width), dtype=bool)
        for ((x0, y0), (x1, y1)) in lines:
            if y0 == y1:
                cave[y0, min(x0, x1):max(x0, x1) + 1] = True
            else:
                cave[min(y0, y1):max(y0, y1) + 1, x0] = True

        return cave,

    def puzzle_1(self, initial_cave: DATA_TYPE) -> int:
        cave = initial_cave.copy()

        try:
            self.simulate_sand_fall(cave, (0, 500))
            raise Exception("Not an infinite fall")
        except RuntimeError:
            return cave.sum() - initial_cave.sum()

    def puzzle_2(self, initial_cave: DATA_TYPE) -> int:
        cave = initial_cave.copy()
        cave[-1, :] = True

        self.simulate_sand_fall(cave, (0, 500))

        return cave[:-1, :].sum() - initial_cave.sum()

    def simulate_sand_fall(self, cave: np.ndarray, start_of_fall: Tuple[int, int]):
        while not cave[start_of_fall]:
            self.simulate_sand_unit_drop(cave, start_of_fall)

    @staticmethod
    def simulate_sand_unit_drop(cave: DATA_TYPE, start: Tuple[int, int]) -> Tuple[int, int]:
        y, x = start

        while y < cave.shape[0] - 1:
            if not cave[y + 1, x]:
                y += 1
            elif not cave[y + 1, x - 1]:
                y += 1
                x -= 1
            elif not cave[y + 1, x + 1]:
                y += 1
                x += 1
            else:
                cave[y, x] = True
                return y, x

        raise RuntimeError("Infinite drop")
