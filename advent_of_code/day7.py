from typing import List, Tuple, Dict
from abstract_puzzles import AbstractPuzzles
from collections import defaultdict

DATA_TYPE = List[Tuple[List[str], int]]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=7,
            puzzle_1_example_answer=95437,
            puzzle_1_answer=919137,
            puzzle_2_example_answer=24933642,
            puzzle_2_answer=2877389,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        data = []

        with open(file_path, 'r') as f:
            command = None
            dir_size = 0
            for line in f.read().splitlines():
                components = line.split(' ')

                if components[0] == '$':
                    if command is not None:
                        data.append((command, dir_size))
                        dir_size = 0

                    command = components[1:]
                else:
                    if components[0] != 'dir':
                        dir_size += int(components[0])

            if command is not None:
                data.append((command, dir_size))

        return data,

    def puzzle_1(self, commands: DATA_TYPE) -> int:
        filesystem = self.parse_commands(commands)

        return sum(filter(lambda dir_size: dir_size <= 100000, filesystem.values()))

    def puzzle_2(self, commands: DATA_TYPE) -> int:
        filesystem = self.parse_commands(commands)

        space_required = 30000000 - (70000000 - filesystem['root'])

        return sorted(filter(lambda dir_size: dir_size >= space_required, filesystem.values()))[0]

    def parse_commands(self, commands: DATA_TYPE) -> Dict[str, int]:
        filesystem = defaultdict(int)

        cwd = ['root']
        for command, dir_size in commands[1:]:  # First command always takes you into the root directory
            if command[0] == 'cd':
                if command[1] == '..':
                    cwd.pop()
                else:
                    cwd.append(command[1])
            elif command[0] == 'ls':
                for directory in self.parent_directories(cwd):
                    filesystem[directory] += dir_size

            else:
                raise Exception(f'Unknown command: {command[0]}')

        return filesystem

    @staticmethod
    def parent_directories(path: List[str]) -> str:
        cwd = path[0]
        yield cwd

        for directory in path[1:]:
            cwd += f'/{directory}'
            yield cwd
