from typing import List, Tuple
from abstract_puzzles import AbstractPuzzles

DATA_TYPE = List[str]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=2,
            puzzle_1_example_answer=15,
            puzzle_1_answer=12679,
            puzzle_2_example_answer=12,
            puzzle_2_answer=14470,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        with open(file_path, 'r') as f:
            return f.read().splitlines(),

    def puzzle_1(self, rounds: DATA_TYPE) -> int:
        round_score = {
            'A X': 4,  # 3 + 1
            'A Y': 8,  # 6 + 2
            'A Z': 3,  # 0 + 3
            'B X': 1,  # 0 + 1
            'B Y': 5,  # 3 + 2
            'B Z': 9,  # 6 + 3
            'C X': 7,  # 6 + 1
            'C Y': 2,  # 0 + 2
            'C Z': 6,  # 3 + 3
        }

        return sum([round_score[_round] for _round in rounds])

    def puzzle_2(self, rounds: DATA_TYPE) -> int:
        round_score = {
            'A X': 3,  # 3 + 0
            'A Y': 4,  # 1 + 3
            'A Z': 8,  # 2 + 6
            'B X': 1,  # 1 + 0
            'B Y': 5,  # 2 + 3
            'B Z': 9,  # 3 + 6
            'C X': 2,  # 2 + 0
            'C Y': 6,  # 3 + 3
            'C Z': 7,  # 1 + 6
        }

        return sum([round_score[_round] for _round in rounds])
