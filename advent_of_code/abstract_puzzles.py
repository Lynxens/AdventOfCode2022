import unittest
from typing import Tuple


class AbstractPuzzles(unittest.TestCase):
    def __init__(
            self,
            method_name: str,
            day: int,
            puzzle_1_example_answer: int | str | None,
            puzzle_1_answer: int | str | None,
            puzzle_2_example_answer: int | str | None,
            puzzle_2_answer: int | str | None,
    ):
        super().__init__(method_name)

        self.day = day
        self.puzzle_1_example_answer = puzzle_1_example_answer
        self.puzzle_1_answer = puzzle_1_answer
        self.puzzle_2_example_answer = puzzle_2_example_answer
        self.puzzle_2_answer = puzzle_2_answer

    def setUp(self) -> None:
        self.data = self.read(f'data/day{self.day}/input.txt')
        self.data_example = self.read(f'data/day{self.day}/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(self.puzzle_1_example_answer, self.puzzle_1(*self.data_example))

    def test_puzzle_1(self):
        self.assertEqual(self.puzzle_1_answer, self.puzzle_1(*self.data))

    def test_puzzle_2_example(self):
        self.assertEqual(self.puzzle_2_example_answer, self.puzzle_2(*self.data_example))

    def test_puzzle_2(self):
        self.assertEqual(self.puzzle_2_answer, self.puzzle_2(*self.data))

    def solve_puzzles(self):
        print(f"Puzzle 1: {self.puzzle_1(*self.data)}")
        print(f"Puzzle 2: {self.puzzle_2(*self.data)}")

    def read(self, file_path: str) -> Tuple:
        raise NotImplementedError

    def puzzle_1(self, *args):
        raise NotImplementedError

    def puzzle_2(self, *args):
        raise NotImplementedError
