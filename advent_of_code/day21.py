from typing import Tuple, Dict, Union
from abstract_puzzles import AbstractPuzzles

DATA_TYPE = Dict[str, Union[int, Tuple[str, str, str]]]

OPERATOR = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b,
}

SOLVE_FOR_RIGHT = {
    '+': lambda a, c: c - a,   # a + b = c -> b = c - a
    '-': lambda a, c: a - c,   # a - b = c -> b = a - c
    '*': lambda a, c: c // a,  # a * b = c -> b = c / a
    '/': lambda a, c: a // c,  # a / b = c -> b = a / c
}

SOLVE_FOR_LEFT = {
    '+': lambda b, c: c - b,   # a + b = c -> a = c - b
    '-': lambda b, c: c + b,   # a - b = c -> a = c + b
    '*': lambda b, c: c // b,  # a * b = c -> a = c / b
    '/': lambda b, c: c * b,   # a / b = c -> a = c * b
}


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=21,
            puzzle_1_example_answer=152,
            puzzle_1_answer=63119856257960,
            puzzle_2_example_answer=301,
            puzzle_2_answer=3006709232464,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        data = {}

        with open(file_path, 'r') as f:
            for line in f.read().splitlines():
                monkey, out = line.split(': ')

                if out.isdigit():
                    data[monkey] = int(out)
                else:
                    data[monkey] = tuple(out.split(' '))

        return data,

    def puzzle_1(self, data: DATA_TYPE) -> int:
        return solve(data, 'root')

    def puzzle_2(self, data: DATA_TYPE) -> int:
        variable = 'humn'

        if includes_variable(data, variable, data['root'][0]):
            start = data['root'][0]
            equal = data['root'][2]
        else:
            start = data['root'][2]
            equal = data['root'][0]

        return solve_for(
            data,
            variable,
            monkey=start,
            equal=solve(data, equal)
        )


def solve(data: DATA_TYPE, monkey: str) -> int:
    value = data[monkey]

    if type(value) is int:
        return value
    else:
        left, operator, right = value

        return int(OPERATOR[operator](solve(data, left), solve(data, right)))


def solve_for(data: DATA_TYPE, variable: str, monkey: str, equal: int) -> int:
    if monkey == variable:
        return equal

    if includes_variable(data, variable, data[monkey][0]):
        right = solve(data, data[monkey][2])

        return solve_for(
            data,
            variable,
            monkey=data[monkey][0],
            equal=SOLVE_FOR_LEFT[data[monkey][1]](right, equal),
        )
    else:
        left = solve(data, data[monkey][0])

        return solve_for(
            data,
            variable,
            monkey=data[monkey][2],
            equal=SOLVE_FOR_RIGHT[data[monkey][1]](left, equal),
        )


def includes_variable(data: DATA_TYPE, variable: str, monkey: str) -> bool:
    if monkey == variable:
        return True

    value = data[monkey]

    if type(value) == int:
        return False
    else:
        left, _, right = value
        return includes_variable(data, variable, left) or includes_variable(data, variable, right)
