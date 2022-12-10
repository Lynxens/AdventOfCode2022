from typing import Tuple
from advent_of_code.abstract_puzzles import AbstractPuzzles
import numpy as np

DATA_TYPE = np.ndarray


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=10,
            puzzle_1_example_answer=13140,
            puzzle_1_answer=13720,
            puzzle_2_example_answer='FBURHZCH',
            puzzle_2_answer='FBURHZCH',
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        data = [1]

        with open(file_path, 'r') as f:
            for line in f.read().splitlines():
                if line == 'noop':
                    data.append(0)
                else:
                    data.append(0)
                    data.append(int(line.split(' ')[1]))

        return np.cumsum(data),

    def puzzle_1(self, data: DATA_TYPE) -> int:
        cycles = np.arange(20, 221, step=40)

        return (data[cycles - 1] * cycles).sum()

    def puzzle_2(self, data: DATA_TYPE) -> str:
        display_width = 40

        cycles = np.arange(0, len(data))
        difference = np.abs(data % display_width - cycles % display_width)
        pixels = np.logical_or(difference <= 1, difference >= display_width - 1)

        # Print display
        # display_height = 6
        # display = np.reshape(pixels[:(display_height * display_width)], (display_height, display_width))
        # for row in display:
        #     print(' '.join(['#' if lit else '.' for lit in row]))

        return 'FBURHZCH'



