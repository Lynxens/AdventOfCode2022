import unittest
from typing import List, Tuple

DAY = 5

STACKS_TYPE = List[List[str]]
INSTRUCTIONS_TYPE = List[Tuple[int, int, int]]


def read(file_path: str) -> Tuple[STACKS_TYPE, INSTRUCTIONS_TYPE]:
    stacks = []
    instructions = []

    with open(file_path, 'r') as f:
        stacks_done = False
        for line in f.read().splitlines():
            if stacks_done:
                instruction = line.split(' ')
                instructions.append((
                    int(instruction[1]),        # Amount
                    int(instruction[3]) - 1,    # From stack
                    int(instruction[5]) - 1,    # To stack
                ))
            elif line == '':
                stacks_done = True
            else:
                stacks.append(list(line))

    return stacks, instructions


def puzzle_1(stacks: STACKS_TYPE, instructions: INSTRUCTIONS_TYPE) -> str:
    for amount, from_stack, to_stack in instructions:
        for i in range(amount):
            stacks[to_stack].append(stacks[from_stack].pop())

    return ''.join([stack[-1] for stack in stacks])


def puzzle_2(stacks: STACKS_TYPE, instructions: INSTRUCTIONS_TYPE) -> str:
    for amount, from_stack, to_stack in instructions:
        stacks[to_stack] += stacks[from_stack][-amount:]
        del stacks[from_stack][-amount:]

    return ''.join([stack[-1] for stack in stacks])


def run():
    data = read(f'data/day{DAY}/input.txt')

    print(f"Puzzle 1: {puzzle_1(*data)}")
    print(f"Puzzle 2: {puzzle_2(*data)}")


class TestPuzzles(unittest.TestCase):
    def setUp(self) -> None:
        self.data = read(f'data/day{DAY}/input.txt')
        self.data_example = read(f'data/day{DAY}/input_example.txt')

    def test_puzzle_1_example(self):
        self.assertEqual(puzzle_1(*self.data_example), 'CMZ')

    def test_puzzle_1(self):
        self.assertEqual(puzzle_1(*self.data), 'FZCMJCRHZ')

    def test_puzzle_2_example(self):
        self.assertEqual(puzzle_2(*self.data_example), 'MCD')

    def test_puzzle_2(self):
        self.assertEqual(puzzle_2(*self.data), 'JSDHQMZGF')


if __name__ == '__main__':
    unittest.main(exit=False)
    run()
