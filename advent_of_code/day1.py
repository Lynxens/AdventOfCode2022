from typing import Tuple, List
from abstract_puzzles import AbstractPuzzles

DATA_TYPE = List[List[int]]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=1,
            puzzle_1_example_answer=24000,
            puzzle_1_answer=69501,
            puzzle_2_example_answer=45000,
            puzzle_2_answer=202346,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        data = [[]]

        with open(file_path, 'r') as f:
            for line in f.readlines():
                if line != '\n':
                    data[-1].append(int(line.strip()))
                else:
                    data.append([])

        return data,

    def puzzle_1(self, food_per_elf: DATA_TYPE) -> int:
        return max([sum(calories) for calories in food_per_elf])

    def puzzle_2(self, food_per_elf: DATA_TYPE) -> int:
        return sum(sorted([sum(calories) for calories in food_per_elf])[-3:])
