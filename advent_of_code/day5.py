from typing import List, Tuple
from abstract_puzzles import AbstractPuzzles

STACKS_TYPE = List[List[str]]
INSTRUCTIONS_TYPE = List[Tuple[int, int, int]]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=5,
            puzzle_1_example_answer='CMZ',
            puzzle_1_answer='FZCMJCRHZ',
            puzzle_2_example_answer='MCD',
            puzzle_2_answer='JSDHQMZGF',
        )

    def read(self, file_path: str) -> Tuple[STACKS_TYPE, INSTRUCTIONS_TYPE]:
        stacks = []
        instructions = []

        with open(file_path, 'r') as f:
            stacks_done = False
            for line in f.read().splitlines():
                if stacks_done:
                    instruction = line.split(' ')
                    instructions.append((
                        int(instruction[1]),  # Amount
                        int(instruction[3]) - 1,  # From stack
                        int(instruction[5]) - 1,  # To stack
                    ))
                elif line == '':
                    stacks_done = True
                else:
                    stacks.append(list(line))

        return stacks, instructions

    def puzzle_1(self, stacks: STACKS_TYPE, instructions: INSTRUCTIONS_TYPE) -> str:
        for amount, from_stack, to_stack in instructions:
            for i in range(amount):
                stacks[to_stack].append(stacks[from_stack].pop())

        return ''.join([stack[-1] for stack in stacks])

    def puzzle_2(self, stacks: STACKS_TYPE, instructions: INSTRUCTIONS_TYPE) -> str:
        for amount, from_stack, to_stack in instructions:
            stacks[to_stack] += stacks[from_stack][-amount:]
            del stacks[from_stack][-amount:]

        return ''.join([stack[-1] for stack in stacks])
