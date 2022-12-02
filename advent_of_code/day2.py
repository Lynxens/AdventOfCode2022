import unittest
from typing import List

DAY = 2


def read(file_path: str) -> List[str]:
    with open(file_path, 'r') as f:
        return f.read().splitlines()


def puzzle_1(rounds: list) -> int:
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


def puzzle_2(rounds: List[str]) -> int:
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


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example = read(f'data/day{DAY}/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.data_example), 15)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 12679)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.data_example), 12)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 14470)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()
