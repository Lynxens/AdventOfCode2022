from typing import List, Tuple
from abstract_puzzles import AbstractPuzzles
from functools import reduce

DATA_TYPE = List[int]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=6,
            puzzle_1_example_answer=7,
            puzzle_1_answer=1175,
            puzzle_2_example_answer=19,
            puzzle_2_answer=3217,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        with open(file_path, 'r') as f:
            return [ord(x) - 97 for x in f.readline()[:-1]],

    def puzzle_1(self, data: DATA_TYPE) -> int:
        return self.find_unique_window(data, window_size=4)

    def puzzle_2(self, data: DATA_TYPE) -> int:
        return self.find_unique_window(data, window_size=14)

    @staticmethod
    def find_unique_window(data: list, window_size: int) -> int:
        bit_vector = reduce(lambda vector, bit: vector ^ (1 << bit), data[:window_size], 0)

        for i in range(window_size, len(data)):
            if bit_vector.bit_count() == window_size:
                return i

            bit_vector ^= 1 << data[i]
            bit_vector ^= 1 << data[i - window_size]

        raise Exception('No unique window found')


