from typing import Tuple, List
from abstract_puzzles import AbstractPuzzles
import numpy as np


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=12,
            puzzle_1_example_answer=31,
            puzzle_1_answer=408,
            puzzle_2_example_answer=29,
            puzzle_2_answer=399,
        )

    def read(self, file_path: str) -> Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]:
        with open(file_path, 'r') as f:
            start = None
            end = None
            data = []

            for i, line in enumerate(f.read().splitlines()):
                line = list(line)

                if 'S' in line:
                    start = (i, line.index('S'))
                    line[start[1]] = 'a'

                if 'E' in line:
                    end = (i, line.index('E'))
                    line[end[1]] = 'z'

                data.append(list(map(ord, line)))

        return np.array(data), start, end,

    def puzzle_1(self, data: np.ndarray, start: Tuple[int, int], end: Tuple[int, int]) -> int:
        return self.breadth_first_search(data, [start], end)

    def puzzle_2(self, data: np.ndarray, _, end: Tuple[int, int]) -> int:
        return self.breadth_first_search(data, list(zip(*np.where(data == ord('a')))), end)

    @staticmethod
    def breadth_first_search(data: np.ndarray, starts: List[Tuple[int, int]], end: Tuple[int, int]) -> int:
        queue = starts
        visited = np.zeros(data.shape, dtype=bool)
        step_count = 0

        while len(queue) > 0:
            coords = set(queue)
            queue = []

            for (y, x) in coords:
                height = data[y, x]

                options = [
                    n for n in [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
                    if 0 <= n[0] < data.shape[0] and 0 <= n[1] < data.shape[1] and data[n] - height <= 1 and not visited[y, x]
                ]

                for option in options:
                    if option == end:
                        return step_count + 1

                    queue.append(option)

                visited[(y, x)] = True

            step_count += 1

        raise Exception(f"No path found after {step_count} steps")
