from typing import Tuple

import numpy as np

from abstract_puzzles import AbstractPuzzles

DATA_TYPE = np.ndarray


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=18,
            puzzle_1_example_answer=64,
            puzzle_1_answer=4604,
            puzzle_2_example_answer=58,
            puzzle_2_answer=2604,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        grid = np.zeros((25, 25, 25), dtype=bool)

        with open(file_path, 'r') as f:
            for line in f.read().splitlines():
                x, y, z = list(map(int, line.split(',')))

                grid[y + 1, x + 1, z + 1] = True

        return grid,

    def puzzle_1(self, data: DATA_TYPE) -> int:
        return sum([np.diff(data, axis=axis).sum() for axis in [0, 1, 2]])

    def puzzle_2(self, data: DATA_TYPE) -> int:
        grid = np.zeros(data.shape, dtype=int)
        queue = [(0, 0, 0)]
        count = 0

        while len(queue) > 0:
            y, x, z = queue.pop(0)

            if not data[y, x, z] and not grid[y, x, z]:
                grid[y, x, z] = True

                for dy, dx, dz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
                    coord = (y + dy, x + dx, z + dz)

                    if 0 <= coord[0] < grid.shape[0] and 0 <= coord[1] < grid.shape[1] and 0 <= coord[2] < grid.shape[2]:
                        if data[coord]:
                            count += 1

                        if not grid[coord]:
                            queue.append(coord)

        return count
