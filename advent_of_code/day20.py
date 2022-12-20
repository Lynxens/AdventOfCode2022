from typing import Tuple, List
from abstract_puzzles import AbstractPuzzles

DATA_TYPE = List[int]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=20,
            puzzle_1_example_answer=3,
            puzzle_1_answer=7225,
            puzzle_2_example_answer=1623178306,
            puzzle_2_answer=548634267428,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        with open(file_path, 'r') as f:
            return list(map(int, f.read().splitlines())),

    def puzzle_1(self, data: DATA_TYPE) -> int:
        return sum(
            get_grove_coordinates(
                data,
                mix_order(data, order=[_ for _ in range(len(data))])
            )
        )

    def puzzle_2(self, _data: DATA_TYPE) -> int:
        decryption_key = 811589153
        mixing_rounds = 10

        data = list(map(lambda x: (x * decryption_key), _data))
        order = [_ for _ in range(len(data))]

        for _ in range(mixing_rounds):
            mix_order(data, order)

        return sum(get_grove_coordinates(data, order))


def mix_order(data: DATA_TYPE, order: List[int]) -> List[int]:
    for i, offset in enumerate(data):
        index = order.index(i)
        new_index = (index + offset) % (len(data) - 1)
        item = order.pop(index)

        if new_index == 0:
            order.append(item)
        else:
            order.insert(new_index, item)

    return order


def get_grove_coordinates(data: DATA_TYPE, order: List[int]) -> List[int]:
    zero_index = order.index(data.index(0))
    return [data[order[(zero_index + j) % len(data)]] for j in [1000, 2000, 3000]]
