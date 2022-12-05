from typing import Tuple, List
from abstract_puzzles import AbstractPuzzles

DATA_TYPE = List[List[int]]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=3,
            puzzle_1_example_answer=157,
            puzzle_1_answer=7878,
            puzzle_2_example_answer=70,
            puzzle_2_answer=2760,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        with open(file_path, 'r') as f:
            return [list(map(self.alphabet_to_number, line)) for line in f.read().splitlines()],

    @staticmethod
    def alphabet_to_number(item: str) -> int:
        return ord(item) - 96 if item.islower() else ord(item) - 38

    def puzzle_1(self, rucksacks: DATA_TYPE) -> int:
        return sum([sum(set.intersection(*compartments)) for compartments in self.compartmented_rucksacks(rucksacks)])

    @staticmethod
    def compartmented_rucksacks(rucksacks: DATA_TYPE):
        for rucksack in rucksacks:
            middle = len(rucksack) // 2
            yield set(rucksack[:middle]), set(rucksack[middle:])

    def puzzle_2(self, rucksacks: DATA_TYPE) -> int:
        return sum([set.intersection(*group).pop() for group in self.elf_groups(rucksacks)])

    @staticmethod
    def elf_groups(rucksacks: DATA_TYPE):
        for i in range(len(rucksacks) // 3):
            yield set(rucksacks[i * 3]), set(rucksacks[i * 3 + 1]), set(rucksacks[i * 3 + 2])
