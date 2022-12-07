from typing import Tuple
from abstract_puzzles import AbstractPuzzles
import numpy as np
from functools import reduce

DATA_TYPE = np.ndarray


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=8,
            puzzle_1_example_answer=21,
            puzzle_1_answer=1538,
            puzzle_2_example_answer=8,
            puzzle_2_answer=496125,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        return np.genfromtxt(file_path, dtype=int, delimiter=1),

    def puzzle_1(self, data: DATA_TYPE) -> int:
        # Accumulative maximum in each direction
        max_left_to_right = np.maximum.accumulate(data, axis=1)
        max_top_to_bottom = np.maximum.accumulate(data, axis=0)
        max_right_to_left = np.flip(np.maximum.accumulate(np.flip(data, axis=1), axis=1), axis=1)
        max_bottom_to_top = np.flip(np.maximum.accumulate(np.flip(data, axis=0), axis=0), axis=0)

        # Count the trees that are the largest in any of the directions
        return np.logical_or.reduce([
            np.diff(max_left_to_right, axis=1, prepend=-1),
            np.diff(max_right_to_left, axis=1, append=-1),
            np.diff(max_top_to_bottom, axis=0, prepend=-1),
            np.diff(max_bottom_to_top, axis=0, append=-1),
        ]).sum()

    def puzzle_2(self, data: DATA_TYPE) -> int:
        best_score = 0
        for row in range(1, data.shape[0] - 1):
            for col in range(1, data.shape[1] - 1):
                tree = data[row, col]

                # Count unobstructed view length in each direction using some numpy magic
                best_score = max(best_score, reduce(
                    lambda prod, view: prod * min(len(view), (~np.maximum.accumulate(view >= tree)).sum() + 1),
                    [
                        data[row, :col][::-1],    # Left
                        data[row, col + 1:],      # Right
                        data[:row, col][::-1],    # Up
                        data[row + 1:, col],      # Down
                    ],
                    1,
                ))

        return best_score
