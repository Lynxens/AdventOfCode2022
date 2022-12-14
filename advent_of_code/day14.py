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

    def puzzle_1(self, _cave: DATA_TYPE) -> int:
        cave = _cave.copy()

        sand_unit_count = 0
        while True:
            y = 0
            x = 500

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
                    sand_unit_count += 1
                    break

            if y >= cave.shape[0] - 1:
                break

        return sand_unit_count

    def puzzle_2(self, _cave: DATA_TYPE) -> int:
        cave = _cave.copy()

        cave[-1, :] = True

        sand_unit_count = 0
        while not cave[0, 500]:
            y = 0
            x = 500

            while not cave[0, 500]:
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
                    sand_unit_count += 1
                    break

        return sand_unit_count
