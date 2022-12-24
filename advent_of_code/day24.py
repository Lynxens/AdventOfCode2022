from typing import Tuple, List, Set
from abstract_puzzles import AbstractPuzzles

DATA_TYPE = List[List[Set[int]]]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=24,
            puzzle_1_example_answer=18,
            puzzle_1_answer=308,
            puzzle_2_example_answer=54,
            puzzle_2_answer=908,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE, DATA_TYPE]:
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()

            grid_height = len(lines) - 2
            grid_width = len(lines[0]) - 2

            grid_ver: DATA_TYPE = [[set() for _ in range(grid_width)] for _ in range(grid_height)]
            grid_hor: DATA_TYPE = [[set() for _ in range(grid_width)] for _ in range(grid_height)]

            for y, line in enumerate(lines[1:-1]):
                for x, c in enumerate(line[1:-1]):
                    if c in '^v':
                        dy = 1 if c == 'v' else -1
                        grid_ver[y][x].add(0)
                        cy = (y + dy) % grid_height
                        t = 1

                        while cy != y:
                            grid_ver[cy][x].add(t)
                            cy = (cy + dy) % grid_height
                            t += 1
                    elif c in '<>':
                        dx = 1 if c == '>' else -1
                        grid_hor[y][x].add(0)
                        cx = (x + dx) % grid_width
                        t = 1

                        while cx != x:
                            grid_hor[y][cx].add(t)
                            cx = (cx + dx) % grid_width
                            t += 1

        return grid_ver, grid_hor

    def puzzle_1(self, grid_ver: DATA_TYPE, grid_hor: DATA_TYPE) -> int:
        return breadth_first_search(grid_ver, grid_hor, start=(-1, 0), end=(len(grid_ver), len(grid_ver[0]) - 1), start_time=0)

    def puzzle_2(self, grid_ver: DATA_TYPE, grid_hor: DATA_TYPE) -> int:
        start = (-1, 0)
        end = (len(grid_ver), len(grid_ver[0]) - 1)

        t1 = breadth_first_search(grid_ver, grid_hor, start, end, start_time=0)
        t2 = breadth_first_search(grid_ver, grid_hor, end, start, start_time=t1)
        t3 = breadth_first_search(grid_ver, grid_hor, start, end, start_time=t2)

        return t3


def breadth_first_search(grid_ver: DATA_TYPE, grid_hor: DATA_TYPE, start: Tuple[int, int], end: Tuple[int, int], start_time: int) -> int:
    height = len(grid_ver)
    width = len(grid_ver[0])
    queue = [start]
    time = start_time

    while len(queue) > 0:
        coords = set(queue)
        queue = []

        next_ver_iteration = (time + 1) % height
        next_hor_iteration = (time + 1) % width

        for (y, x) in coords:
            options = [
                n for n in [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1), (y, x)]
                if n == start or n == end or (
                        0 <= n[0] < height and
                        0 <= n[1] < width and
                        next_ver_iteration not in grid_ver[n[0]][n[1]] and
                        next_hor_iteration not in grid_hor[n[0]][n[1]]
                )
            ]

            for option in options:
                if option == end:
                    return time + 1

                queue.append(option)

        time += 1

    raise Exception(f"No path found after {time} minutes")
