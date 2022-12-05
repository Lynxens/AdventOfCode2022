from typing import Tuple
from abstract_puzzles import AbstractPuzzles

DATA_TYPE = None


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=None,
            puzzle_1_example_answer=None,
            puzzle_1_answer=None,
            puzzle_2_example_answer=None,
            puzzle_2_answer=None,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        with open(file_path, 'r') as f:
            return f.read().splitlines(),

    def puzzle_1(self, data: DATA_TYPE) -> int:
        pass

    def puzzle_2(self, data: DATA_TYPE) -> int:
        pass
