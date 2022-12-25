from typing import Tuple, List
from abstract_puzzles import AbstractPuzzles

DATA_TYPE = List[str]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=25,
            puzzle_1_example_answer='2=-1=0',
            puzzle_1_answer='2=01-0-2-0=-0==-1=01',
            puzzle_2_example_answer=None,
            puzzle_2_answer=None,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        with open(file_path, 'r') as f:
            return f.read().splitlines(),

    def puzzle_1(self, data: DATA_TYPE) -> str:
        return lazy_encode(sum([decode(v) for v in data]))

    def puzzle_2(self, data: DATA_TYPE) -> int:
        pass


def decode(encoded: str) -> int:
    return sum([
        value * pow(5, power)
        for power, value in enumerate(reversed([int(c.replace('-', '-1').replace('=', '-2')) for c in encoded]))
    ])

# WIP
# def encode(decoded: int) -> str:
#     start_power = 0
#     while 2 * pow(5, start_power) < decoded:
#         start_power += 1
#
#     encoded = []
#     total = 0
#     for power in range(start_power, -1, -1):
#         if total == decoded:
#             encoded.append('0')
#         elif total > decoded:
#             remainder = decoded - total
#
#             if -pow(5, power) < remainder :
#                 total -= 2 * pow(5, power)
#                 encoded.append('=')
#             elif -pow(5, power) <= remainder < (-2 * pow(5, power - 1) if power > 0 else 0):
#                 total -= pow(5, power)
#                 encoded.append('-')
#             else:
#                 encoded.append('0')
#         else:
#             remainder = decoded - total
#
#             if remainder > pow(5, power):
#                 total += 2 * pow(5, power)
#                 encoded.append('2')
#             elif ((2 * pow(5, power - 1)) if power > 0 else 0) < remainder <= pow(5, power):
#                 total += pow(5, power)
#                 encoded.append('1')
#             else:
#                 encoded.append('0')
#
#     assert total == decoded
#
#     return ''.join(encoded)


def lazy_encode(decoded: int) -> str:
    start_power = 0
    while 2 * pow(5, start_power) < decoded:
        start_power += 1

    found, encoded = lazy_encode_nested(decoded, start_power)

    if not found:
        raise Exception('No encoding found')

    return ''.join(encoded)


def lazy_encode_nested(remainder: int, depth: int) -> Tuple[bool, List[str]]:
    if depth < 0:
        return remainder == 0, []

    if remainder > 3 * pow(5, depth) or remainder < -3 * pow(5, depth):
        return False, []

    if remainder > 0:
        for value, i in [('2', 2), ('1', 1), ('0', 0)]:
            found, encoded = lazy_encode_nested(remainder - i * pow(5, depth), depth - 1)

            if found:
                encoded.insert(0, value)

                return True, encoded
    else:
        for value, i in [('0', 0), ('-', -1), ('=', -2)]:
            found, encoded = lazy_encode_nested(remainder - i * pow(5, depth), depth - 1)

            if found:
                encoded.insert(0, value)

                return True, encoded

    return False, []

