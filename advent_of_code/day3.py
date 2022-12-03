import unittest
from typing import List

DAY = 3
DATA_TYPE = List[List[int]]


def alphabet_to_number(item: str) -> int:
    return ord(item) - 96 if item.islower() else ord(item) - 38


def read(file_path: str) -> DATA_TYPE:
    with open(file_path, 'r') as f:
        return [list(map(alphabet_to_number, line)) for line in f.read().splitlines()]


def puzzle_1(rucksacks: DATA_TYPE) -> int:
    return sum([sum(set.intersection(*compartments)) for compartments in compartmented_rucksacks(rucksacks)])


def compartmented_rucksacks(rucksacks: DATA_TYPE):
    for rucksack in rucksacks:
        middle = len(rucksack) // 2
        yield set(rucksack[:middle]), set(rucksack[middle:])


def puzzle_2(rucksacks: DATA_TYPE) -> int:
    return sum([set.intersection(*group).pop() for group in elf_groups(rucksacks)])


def elf_groups(rucksacks: DATA_TYPE):
    for i in range(len(rucksacks) // 3):
        yield set(rucksacks[i * 3]), set(rucksacks[i * 3 + 1]), set(rucksacks[i * 3 + 2])


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example = read(f'data/day{DAY}/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.data_example), 157)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 7878)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.data_example), 70)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 2760)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()
