from typing import Tuple, List
from abstract_puzzles import AbstractPuzzles
import numpy as np

DATA_TYPE = List[int]

"""
Index 0 -> Left most
Index 1 -> Bottom
Index -2 -> Top
Index -1 -> Right most
"""
LEFT = 0
BOTTOM = 1
TOP = -2
RIGHT = -1

SHAPES = {
    '-': lambda bottom: (
        np.array([bottom] * 4),
        np.array([2, 3, 4, 5])
    ),
    '+': lambda bottom: (
        np.array([bottom + 1, bottom, bottom + 1, bottom + 2, bottom + 1]),
        np.array([2, 3, 3, 3, 4])
    ),
    '_|': lambda bottom: (
        np.array([bottom, bottom, bottom, bottom + 2, bottom + 1]),
        np.array([2, 3, 4, 4, 4])
    ),
    '|': lambda bottom: (
        np.array([bottom + 1, bottom, bottom + 3, bottom + 2]),
        np.array([2] * 4)
    ),
    'O': lambda bottom: (
        np.array([bottom + 1, bottom, bottom + 1, bottom]),
        np.array([2, 2, 3, 3])
    ),
}


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=17,
            puzzle_1_example_answer=3068,
            puzzle_1_answer=3130,
            puzzle_2_example_answer=1514285714288,
            puzzle_2_answer=1556521739139,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        with open(file_path, 'r') as f:
            return [-1 if direction == '<' else 1 for direction in f.read()],

    def puzzle_1(self, jetstream: DATA_TYPE) -> int:
        return simulate_rocks(jetstream, number_of_rocks=2022)[0][-1]

    def puzzle_2(self, jetstream: DATA_TYPE) -> int:
        step_offset, step_increment, height_offset, height_increment = find_cycle(jetstream)

        height = height_offset + ((1000000000000 - step_offset) // step_increment) * height_increment
        steps_left = (1000000000000 - step_offset) % step_increment

        height += simulate_rocks(jetstream, step_offset + steps_left)[0][-1] - height_offset

        return height


def find_cycle(jetstream: DATA_TYPE) -> Tuple[int, int, int, int]:
    # We should be able to find a cycle after 6000 rocks have dropped
    number_of_rocks = 6000
    heights, shape_indices, jet_indices = simulate_rocks(jetstream, number_of_rocks)
    height_increments = np.diff(heights)

    for i in range(number_of_rocks):
        cycle_indices = np.where(
            np.logical_and(
                shape_indices[1:] == shape_indices[i],
                jet_indices[1:] == jet_indices[i],
                height_increments == height_increments[i]
            )
        )

        if len(cycle_indices[0]) > 2:
            dropped_rocks_count_cycle = np.diff(cycle_indices[0])
            height_increment_cycle = np.diff(heights[cycle_indices[0]])

            return dropped_rocks_count_cycle[0], dropped_rocks_count_cycle[1], height_increment_cycle[0], height_increment_cycle[1]

    raise Exception("No cycle found")


def simulate_rocks(jetstream: DATA_TYPE, number_of_rocks: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    shape_order = ['-', '+', '_|', '|', 'O']
    chamber_width = 7
    max_rock_height = 4

    chamber = np.zeros((number_of_rocks * max_rock_height, chamber_width), dtype=bool)

    step = 0

    shape_indices = [0]
    jet_indices = [0]
    heights = [0]
    for rock in range(number_of_rocks):
        y, x = SHAPES[shape_order[rock % len(shape_order)]](heights[-1] + 3)

        while True:
            next_x = x + jetstream[step % len(jetstream)]
            step += 1

            if next_x[LEFT] >= 0 and next_x[RIGHT] < chamber_width and not chamber[y, next_x].max():
                x = next_x

            next_y = y - 1

            if next_y[BOTTOM] < 0 or chamber[next_y, x].max():
                break

            y = next_y

        chamber[y, x] = True
        shape_indices.append(rock % len(shape_order))
        jet_indices.append(step % len(jetstream))
        heights.append(max(heights[-1], y[TOP] + 1))

    return np.array(heights), np.array(shape_indices), np.array(jet_indices)
