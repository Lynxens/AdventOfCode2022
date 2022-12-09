from typing import List, Tuple
from abstract_puzzles import AbstractPuzzles
import numpy as np

DATA_TYPE = List[np.ndarray]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=9,
            puzzle_1_example_answer=13,
            puzzle_1_answer=6271,
            puzzle_2_example_answer=1,
            puzzle_2_answer=2458,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        dydx = {
            'U': np.array([1, 0]),
            'D': np.array([-1, 0]),
            'L': np.array([0, -1]),
            'R': np.array([0, 1]),
        }

        directions = []

        with open(file_path, 'r') as f:
            for line in f.read().splitlines():
                direction, steps = line.split(' ')
                directions += [dydx[direction]] * int(steps)

        return directions,

    def puzzle_1(self, directions: DATA_TYPE) -> int:
        return self.simulate_rope(directions, rope_length=2)

    def puzzle_2(self, directions: DATA_TYPE) -> int:
        return self.simulate_rope(directions, rope_length=10)

    @staticmethod
    def simulate_rope(directions: DATA_TYPE, rope_length: int) -> int:
        rope = np.zeros((rope_length, 2), dtype=int)
        t_locs = set()

        for direction in directions:
            rope[0] += direction

            for i in range(1, rope_length):
                dydx = rope[i - 1] - rope[i]

                if not (-1 <= dydx[0] <= 1 and -1 <= dydx[1] <= 1):
                    rope[i] += np.sign(dydx)

            t_locs.add(tuple(rope[-1]))

        return len(t_locs)

    def test_puzzle_2_example2(self):
        data = self.read(f'data/day{self.day}/input_example2.txt')
        self.assertEqual(36, self.puzzle_2(*data))
