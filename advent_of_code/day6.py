from typing import Tuple
from abstract_puzzles import AbstractPuzzles

DATA_TYPE = list


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
            return list(f.readline()[:-1]),

    def puzzle_1(self, data: DATA_TYPE) -> int:
        for i, window in self.window_slider(data, 4):
            if len(set(window)) == 4:
                return i

        raise Exception('No start of packet found')

    def puzzle_2(self, data: DATA_TYPE) -> int:
        for i, window in self.window_slider(data, 14):
            if len(set(window)) == 14:
                return i

        raise Exception('No start of message found')

    @staticmethod
    def window_slider(data: list, window_size: int) -> Tuple[int, list]:
        window = list(data[:window_size])

        for i, element in enumerate(data[window_size:], window_size):
            yield i, window

            window.append(element)
            window.pop(0)


