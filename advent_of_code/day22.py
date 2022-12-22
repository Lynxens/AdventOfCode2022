from typing import Tuple, List
import numpy as np
from abstract_puzzles import AbstractPuzzles
import re

DATA_TYPE = np.ndarray
DIRECTIONS_TYPE = List[str]

EMPTY = 0
PATH = 1
WALL = 2

RIGHT = np.array([0, 1], dtype=int)
DOWN = np.array([1, 0], dtype=int)
LEFT = np.array([0, -1], dtype=int)
UP = np.array([-1, 0], dtype=int)

TO_RIGHT = {
    tuple(RIGHT): DOWN,
    tuple(DOWN): LEFT,
    tuple(LEFT): UP,
    tuple(UP): RIGHT,
}

TO_LEFT = {
    tuple(RIGHT): UP,
    tuple(UP): LEFT,
    tuple(LEFT): DOWN,
    tuple(DOWN): RIGHT,
}


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=22,
            puzzle_1_example_answer=6032,
            puzzle_1_answer=88268,
            puzzle_2_example_answer=5031,
            puzzle_2_answer=124302,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE, DIRECTIONS_TYPE]:
        with open(file_path, 'r') as f:
            cave, directions = f.read().split('\n\n')

            cave_rows = cave.split('\n')

            data = np.zeros((len(cave_rows), max(map(len, cave_rows))), dtype=int)
            for i, row in enumerate(cave_rows):
                for j, item in enumerate(row):
                    if item == '.':
                        data[i, j] = PATH
                    elif item == '#':
                        data[i, j] = WALL

            return data, re.findall(r"(L|R|\d+)", directions)

    def puzzle_1(self, cave: DATA_TYPE, directions: DATA_TYPE) -> int:
        position = np.array(list(zip(*np.where(cave == 1)))[0])

        orientation = RIGHT

        for direction in directions:
            if direction == 'L':
                orientation = TO_LEFT[tuple(orientation)]
            elif direction == 'R':
                orientation = TO_RIGHT[tuple(orientation)]
            else:
                for _ in range(int(direction)):
                    new_position = position + orientation

                    if new_position[0] < 0 or new_position[0] >= cave.shape[0] or new_position[1] < 0 or new_position[1] >= cave.shape[1] or cave[tuple(new_position)] == EMPTY:
                        new_position -= orientation

                        while 0 <= new_position[0] < cave.shape[0] and 0 <= new_position[1] < cave.shape[1] and cave[tuple(new_position)] != EMPTY:
                            new_position -= orientation

                        new_position += orientation

                    if cave[tuple(new_position)] == WALL:
                        break

                    position = new_position

        return 1000 * (position[0] + 1) + 4 * (position[1] + 1) + {tuple(RIGHT): 0, tuple(DOWN): 1, tuple(LEFT): 2, tuple(UP): 3}[tuple(orientation)]

    def puzzle_2(self, cave: DATA_TYPE, directions: DATA_TYPE) -> int:
        position = np.array(list(zip(*np.where(cave == 1)))[0])

        orientation = RIGHT

        for direction in directions:
            if direction == 'L':
                orientation = TO_LEFT[tuple(orientation)]
            elif direction == 'R':
                orientation = TO_RIGHT[tuple(orientation)]
            else:
                for _ in range(int(direction)):
                    new_position = position + orientation

                    if new_position[0] < 0 or new_position[0] >= cave.shape[0] or new_position[1] < 0 or new_position[1] >= cave.shape[1] or cave[tuple(new_position)] == EMPTY:
                        if cave.shape[1] == 16:
                            new_position, new_orientation = wrap_example(new_position)
                        else:
                            new_position, new_orientation = wrap(new_position)

                        if cave[tuple(new_position)] == WALL:
                            break

                        orientation = new_orientation

                    if cave[tuple(new_position)] == WALL:
                        break

                    position = new_position

        return 1000 * (position[0] + 1) + 4 * (position[1] + 1) + {tuple(RIGHT): 0, tuple(DOWN): 1, tuple(LEFT): 2, tuple(UP): 3}[tuple(orientation)]


def wrap_example(position: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    edges = {
        '1_top': {
            'x1': 8,
            'x2': 11,
            'y1': -1,
            'y2': -1,
            'wrap': lambda dy, dx: (np.array([edges['2_top']['y1'], edges['2_top']['x2'] - dx]) + DOWN, DOWN)
        },
        '1_right': {
            'x1': 12,
            'x2': 12,
            'y1': 0,
            'y2': 3,
            'wrap': lambda dy, dx: (np.array([edges['6_right']['y2'] - dy, edges['6_right']['x2']]) + LEFT, LEFT)
        },
        '1_left': {
            'x1': 7,
            'x2': 7,
            'y1': 0,
            'y2': 3,
            'wrap': lambda dy, dx: (np.array([edges['3_top']['y1'], edges['3_top']['x1'] + dy]) + DOWN, DOWN)
        },
        '2_top': {
            'x1': 0,
            'x2': 3,
            'y1': 3,
            'y2': 3,
            'wrap': lambda dy, dx: (np.array([edges['1_top']['y1'], edges['1_top']['x2'] - dx]) + DOWN, DOWN)
        },
        '2_bottom': {
            'x1': 0,
            'x2': 3,
            'y1': 8,
            'y2': 8,
            'wrap': lambda dy, dx: (np.array([edges['5_bottom']['y2'], edges['5_bottom']['x2'] - dx]) + UP, UP)
        },
        '2_left': {
            'x1': -1,
            'x2': -1,
            'y1': 4,
            'y2': 7,
            'wrap': lambda dy, dx: (np.array([edges['6_bottom']['y2'], edges['6_bottom']['x2'] - dy]) + UP, UP)
        },
        '3_top': {
            'x1': 4,
            'x2': 7,
            'y1': 3,
            'y2': 3,
            'wrap': lambda dy, dx: (np.array([edges['1_left']['y1'] + dx, edges['1_left']['x1']]) + RIGHT, RIGHT)
        },
        '3_bottom': {
            'x1': 4,
            'x2': 7,
            'y1': 8,
            'y2': 8,
            'wrap': lambda dy, dx: (np.array([edges['5_left']['y2'] - dx, edges['5_left']['x1']]) + RIGHT, RIGHT)
        },
        '4_right': {
            'x1': 12,
            'x2': 12,
            'y1': 4,
            'y2': 7,
            'wrap': lambda dy, dx: (np.array([edges['6_top']['y1'], edges['6_top']['x2'] - dy]) + DOWN, DOWN)
        },
        '5_bottom': {
            'x1': 8,
            'x2': 11,
            'y1': 12,
            'y2': 12,
            'wrap': lambda dy, dx: (np.array([edges['2_bottom']['y2'], edges['2_bottom']['x2'] - dx]) + UP, UP)
        },
        '5_left': {
            'x1': 7,
            'x2': 7,
            'y1': 8,
            'y2': 11,
            'wrap': lambda dy, dx: (np.array([edges['3_bottom']['y2'], edges['3_bottom']['x2'] - dy]) + UP, UP)
        },
        '6_top': {
            'x1': 12,
            'x2': 15,
            'y1': 7,
            'y2': 7,
            'wrap': lambda dy, dx: (np.array([edges['4_right']['y2'] - dx, edges['4_right']['x2']]) + LEFT, LEFT)
        },
        '6_right': {
            'x1': 16,
            'x2': 16,
            'y1': 8,
            'y2': 11,
            'wrap': lambda dy, dx: (np.array([edges['1_right']['y2'] - dy, edges['1_right']['x2']]) + LEFT, LEFT)
        },
        '6_bottom': {
            'x1': 12,
            'x2': 15,
            'y1': 12,
            'y2': 12,
            'wrap': lambda dy, dx: (np.array([edges['2_left']['y2'] - dx, edges['2_left']['x1']]) + RIGHT, RIGHT)
        },
    }

    for edge in edges.values():
        if edge['y1'] <= position[0] <= edge['y2'] and edge['x1'] <= position[1] <= edge['x2']:
            return edge['wrap'](position[0] - edge['y1'], position[1] - edge['x1'])

    raise Exception("Unexpected edge")


def wrap(position: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    edges = {
        '1_top': {
            'x1': 50,
            'x2': 99,
            'y1': -1,
            'y2': -1,
            'wrap': lambda dy, dx: (np.array([edges['6_left']['y1'] + dx, edges['6_left']['x1']]) + RIGHT, RIGHT)
        },
        '1_left': {
            'x1': 49,
            'x2': 49,
            'y1': 0,
            'y2': 49,
            'wrap': lambda dy, dx: (np.array([edges['5_left']['y2'] - dy, edges['5_left']['x1']]) + RIGHT, RIGHT)
        },
        '2_top': {
            'x1': 100,
            'x2': 149,
            'y1': -1,
            'y2': -1,
            'wrap': lambda dy, dx: (np.array([edges['6_bottom']['y2'], edges['6_bottom']['x1'] + dx]) + UP, UP)
        },
        '2_right': {
            'x1': 150,
            'x2': 150,
            'y1': 0,
            'y2': 49,
            'wrap': lambda dy, dx: (np.array([edges['4_right']['y2'] - dy, edges['4_right']['x2']]) + LEFT, LEFT)
        },
        '2_bottom': {
            'x1': 100,
            'x2': 149,
            'y1': 50,
            'y2': 50,
            'wrap': lambda dy, dx: (np.array([edges['3_right']['y1'] + dx, edges['3_right']['x2']]) + LEFT, LEFT)
        },
        '3_left': {
            'x1': 49,
            'x2': 49,
            'y1': 50,
            'y2': 99,
            'wrap': lambda dy, dx: (np.array([edges['5_top']['y1'], edges['5_top']['x1'] + dy]) + DOWN, DOWN)
        },
        '3_right': {
            'x1': 100,
            'x2': 100,
            'y1': 50,
            'y2': 99,
            'wrap': lambda dy, dx: (np.array([edges['2_bottom']['y2'], edges['2_bottom']['x1'] + dy]) + UP, UP)
        },
        '4_right': {
            'x1': 100,
            'x2': 100,
            'y1': 100,
            'y2': 149,
            'wrap': lambda dy, dx: (np.array([edges['2_right']['y2'] - dy, edges['2_right']['x2']]) + LEFT, LEFT)
        },
        '4_bottom': {
            'x1': 50,
            'x2': 99,
            'y1': 150,
            'y2': 150,
            'wrap': lambda dy, dx: (np.array([edges['6_right']['y1'] + dx, edges['6_right']['x2']]) + LEFT, LEFT)
        },
        '5_top': {
            'x1': 0,
            'x2': 49,
            'y1': 99,
            'y2': 99,
            'wrap': lambda dy, dx: (np.array([edges['3_left']['y1'] + dx, edges['3_left']['x1']]) + RIGHT, RIGHT)
        },
        '5_left': {
            'x1': -1,
            'x2': -1,
            'y1': 100,
            'y2': 149,
            'wrap': lambda dy, dx: (np.array([edges['1_left']['y2'] - dy, edges['1_left']['x1']]) + RIGHT, RIGHT)
        },
        '6_right': {
            'x1': 50,
            'x2': 50,
            'y1': 150,
            'y2': 199,
            'wrap': lambda dy, dx: (np.array([edges['4_bottom']['y2'], edges['4_bottom']['x1'] + dy]) + UP, UP)
        },
        '6_bottom': {
            'x1': 0,
            'x2': 49,
            'y1': 200,
            'y2': 200,
            'wrap': lambda dy, dx: (np.array([edges['2_top']['y1'], edges['2_top']['x1'] + dx]) + DOWN, DOWN)
        },
        '6_left': {
            'x1': -1,
            'x2': -1,
            'y1': 150,
            'y2': 199,
            'wrap': lambda dy, dx: (np.array([edges['1_top']['y1'], edges['1_top']['x1'] + dy]) + DOWN, DOWN)
        },
    }

    for edge in edges.values():
        if edge['y1'] <= position[0] <= edge['y2'] and edge['x1'] <= position[1] <= edge['x2']:
            return edge['wrap'](position[0] - edge['y1'], position[1] - edge['x1'])

    raise Exception("Unexpected edge")