import json
from typing import Tuple, List
from abstract_puzzles import AbstractPuzzles


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=13,
            puzzle_1_example_answer=13,
            puzzle_1_answer=5717,
            puzzle_2_example_answer=140,
            puzzle_2_answer=25935,
        )

    def read(self, file_path: str) -> Tuple[List[Tuple[list, list]]]:
        data = []

        with open(file_path, 'r') as f:
            for pair in f.read().split('\n\n'):
                left, right = pair.split('\n')
                data.append((Packet(json.loads(left)), Packet(json.loads(right))))

        return data,

    def puzzle_1(self, data: List[Tuple[list, list]]) -> int:
        return sum([i for i, (left, right) in enumerate(data, 1) if left < right])

    def puzzle_2(self, data: List[Tuple[list, list]]) -> int:
        divider_1 = Packet([[2]])
        divider_2 = Packet([[6]])

        sorted_packets = sorted(list(sum(data, ())) + [divider_1, divider_2])

        return (sorted_packets.index(divider_1) + 1) * (sorted_packets.index(divider_2) + 1)


class Packet(list):
    def __init__(self, *args):
        super().__init__((Packet(arg) if type(arg) is list else arg) for arg in (args[0] if len(args) == 1 else args))

    # Returns None if the index does not exist
    def __getitem__(self, key) -> list | int | None:
        if type(key) is int:
            return super().__getitem__(key) if key < super().__len__() else None

        if len(key) == 1:
            return super().__getitem__(key[0]) if key[0] < super().__len__() else None

        return self.__getitem__(key[0])[key[1:]] if key[0] < self.__len__() else None

    def __setitem__(self, key, value):
        if type(key) is int:
            super().__setitem__(key, value)
            return

        if len(key) == 1:
            super().__setitem__(key[0], value)
            return

        self.__getitem__(key[0]).__setitem__(key[1:], value)

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __cmp__(self, other):
        left = Packet(self.copy())
        right = Packet(other.copy())

        index = [0]

        while len(index) > 0:
            left_element = left[index]
            right_element = right[index]

            if left_element is None or right_element is None:
                if left_element is None and right_element is None:
                    index.pop()

                    if len(index) == 0:
                        break

                    index[-1] += 1
                    continue

                return -1 if left_element is None else 1

            if type(left_element) is int and type(right_element) is int:
                if left_element == right_element:
                    index[-1] += 1
                else:
                    return -1 if left_element < right_element else 1
            else:
                if type(left_element) is int:
                    left[index] = Packet([left_element])

                if type(right_element) is int:
                    right[index] = Packet([right_element])

                index.append(0)

        return 0
