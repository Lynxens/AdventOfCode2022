import unittest
from typing import List

DATA_TYPE = List[List[int]]
DAY = 1


def read(file_path: str) -> DATA_TYPE:
    data = [[]]

    with open(file_path, 'r') as f:
        for line in f.readlines():
            if line != '\n':
                data[-1].append(int(line.strip()))
            else:
                data.append([])

    return data


def puzzle_1(food_per_elf: DATA_TYPE) -> int:
    return max([sum(calories) for calories in food_per_elf])


def puzzle_2(food_per_elf: DATA_TYPE) -> int:
    return sum(sorted([sum(calories) for calories in food_per_elf])[-3:])


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example = read(f'data/day{DAY}/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.data_example), 24000)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 69501)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.data_example), 45000)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 202346)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()

