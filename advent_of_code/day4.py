from typing import List, Tuple
from abstract_puzzles import AbstractPuzzles

DATA_TYPE = List[Tuple[Tuple[int, int], Tuple[int, int]]]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=4,
            puzzle_1_example_answer=2,
            puzzle_1_answer=487,
            puzzle_2_example_answer=4,
            puzzle_2_answer=849,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
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

        return data,

    def puzzle_1(self, schedules: DATA_TYPE) -> int:
        return len(list(filter(
            lambda elfs: (elfs[0][0] >= elfs[1][0] and elfs[0][1] <= elfs[1][1]) or
                         (elfs[1][0] >= elfs[0][0] and elfs[1][1] <= elfs[0][1]),
            schedules
        )))

    def puzzle_2(self, schedules: DATA_TYPE) -> int:
        return len(list(filter(
            lambda elfs: elfs[1][0] <= elfs[0][0] <= elfs[1][1] or
                         elfs[1][0] <= elfs[0][1] <= elfs[1][1] or
                         elfs[0][0] <= elfs[1][0] <= elfs[0][1] or
                         elfs[0][0] <= elfs[1][1] <= elfs[0][1],
            schedules
        )))
