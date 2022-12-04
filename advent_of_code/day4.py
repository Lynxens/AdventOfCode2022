import unittest
from typing import List, Tuple

DAY = 4
DATA_TYPE = List[Tuple[Tuple[int, int], Tuple[int, int]]]


def read(file_path: str) -> DATA_TYPE:
    data = []

    with open(file_path, 'r') as f:
        for line in f.read().splitlines():
            elf1, elf2 = line.split(',')
            elf1_start, elf1_end = elf1.split('-')
            elf2_start, elf2_end = elf2.split('-')

            data.append((
                (int(elf1_start), int(elf1_end)),
                (int(elf2_start), int(elf2_end)),
            ))

    return data


def puzzle_1(schedules: DATA_TYPE) -> int:
    return len(list(filter(
        lambda elfs: (elfs[0][0] >= elfs[1][0] and elfs[0][1] <= elfs[1][1]) or
                     (elfs[1][0] >= elfs[0][0] and elfs[1][1] <= elfs[0][1]),
        schedules
    )))


def puzzle_2(schedules: DATA_TYPE) -> int:
    return len(list(filter(
        lambda elfs: elfs[1][0] <= elfs[0][0] <= elfs[1][1] or
                     elfs[1][0] <= elfs[0][1] <= elfs[1][1] or
                     elfs[0][0] <= elfs[1][0] <= elfs[0][1] or
                     elfs[0][0] <= elfs[1][1] <= elfs[0][1],
        schedules
    )))


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(data)}")
    print(f"Puzzle 2: {puzzle_2(data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example = read(f'data/day{DAY}/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(self.data_example), 2)

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(self.data), 487)

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(self.data_example), 4)

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(self.data), 849)


if __name__ == '__main__':
    unittest.main(exit=False)
    run()
