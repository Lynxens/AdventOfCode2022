from typing import Tuple, Set
from abstract_puzzles import AbstractPuzzles

DATA_TYPE = Set[Tuple[int, int]]

ELF_DIRECTIONS = [
    lambda c: [(c[0] - 1, c[1] - 1), (c[0] - 1, c[1]), (c[0] - 1, c[1] + 1)],  # North
    lambda c: [(c[0] + 1, c[1] - 1), (c[0] + 1, c[1]), (c[0] + 1, c[1] + 1)],  # South
    lambda c: [(c[0] - 1, c[1] - 1), (c[0], c[1] - 1), (c[0] + 1, c[1] - 1)],  # West
    lambda c: [(c[0] - 1, c[1] + 1), (c[0], c[1] + 1), (c[0] + 1, c[1] + 1)],  # East
]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=23,
            puzzle_1_example_answer=110,
            puzzle_1_answer=3812,
            puzzle_2_example_answer=20,
            puzzle_2_answer=1003,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        data = set()

        with open(file_path, 'r') as f:
            for i, line in enumerate(f.read().splitlines()):
                for j, c in enumerate(line):
                    if c == '#':
                        data.add((i, j))

        return data,

    def puzzle_1(self, data: DATA_TYPE) -> int:
        elfs = data.copy()

        for round in range(10):
            elfs_next = elf_diffusion(elfs, round)

            assert len(elfs) == len(elfs_next)
            elfs = elfs_next

        ys = [e[0] for e in elfs]
        xs = [e[1] for e in elfs]
        return (max(ys) - min(ys) + 1) * (max(xs) - min(xs) + 1) - len(elfs)

    def puzzle_2(self, data: DATA_TYPE) -> int:
        elfs = data.copy()

        round = 0
        while True:
            elfs_next = elf_diffusion(elfs, round)
            round += 1

            stationary_elfs = elfs & elfs_next
            if len(stationary_elfs) == len(elfs):
                break

            elfs = elfs_next

        return round


def elf_diffusion(elfs: DATA_TYPE, round: int) -> DATA_TYPE:
    stationary_elfs = set()
    moving_elfs = set()
    moving_proposals = {}

    for elf_position in elfs:
        open_directions = [
            n[1]
            for n in [ELF_DIRECTIONS[direction % 4](elf_position) for direction in range(round, round + 4)]
            if len(set(n) & elfs) == 0
        ]

        if len(open_directions) == 0 or len(open_directions) == 4:
            stationary_elfs.add(elf_position)
            continue

        next_position = open_directions[0]

        if next_position in moving_proposals:
            if next_position in moving_elfs:
                moving_elfs.remove(next_position)

            stationary_elfs.add(elf_position)
            stationary_elfs.add(moving_proposals[next_position])
        else:
            moving_elfs.add(next_position)
            moving_proposals[next_position] = elf_position

    return set.union(stationary_elfs, moving_elfs)
