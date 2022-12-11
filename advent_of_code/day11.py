from typing import List, Tuple, Dict, Any
from abstract_puzzles import AbstractPuzzles
import re


class Monkey:
    def __init__(self, exchange, identifier: int, items: List[Any], operator_type: str, operation_value: int, divisible_by: int, on_true: int, on_false: int):
        self.exchange = exchange
        self.identifier = identifier
        self.items = items
        self.operation = {
            '*': lambda a, b: a * b,
            '+': lambda a, b: a + b,
            '**': lambda a, b: a ** b,
        }[operator_type]
        self.operation_value = operation_value
        self.divisible_by = divisible_by
        self.on_true = on_true
        self.on_false = on_false
        self.number_of_inspected_items = 0

    def add_item(self, item: int):
        self.items.append(item)

    def process_items_puzzle_1(self):
        while len(self.items) > 0:
            old_value = self.items.pop(0)
            self.number_of_inspected_items += 1

            new_value = self.operation(old_value, self.operation_value) // 3

            self.exchange.exchange_item(
                new_value,
                self.on_true if new_value % self.divisible_by == 0 else self.on_false,
            )

    def process_items_puzzle_2(self):
        while len(self.items) > 0:
            old_values = self.items.pop(0)
            self.number_of_inspected_items += 1

            new_values = [self.operation(value, self.operation_value) % self.exchange.monkeys[i].divisible_by for i, value in enumerate(old_values)]

            self.exchange.exchange_item(
                new_values,
                self.on_true if new_values[self.identifier] == 0 else self.on_false,
            )


class Exchange:
    def __init__(self):
        self.monkeys: Dict[int, Monkey] = {}

    def add_monkey(self, identifier: int, monkey: Monkey):
        self.monkeys[identifier] = monkey

    def exchange_item(self, item: Any, to_monkey: int):
        self.monkeys[to_monkey].add_item(item)

    def run_round_puzzle_1(self):
        for i in range(len(self.monkeys)):
            self.monkeys[i].process_items_puzzle_1()

    def setup_round_2(self):
        for monkey in self.monkeys.values():
            for i, item in enumerate(monkey.items):
                monkey.items[i] = [item % m.divisible_by for m in self.monkeys.values()]

    def run_round_puzzle_2(self):
        for i in range(len(self.monkeys)):
            self.monkeys[i].process_items_puzzle_2()


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=11,
            puzzle_1_example_answer=10605,
            puzzle_1_answer=113232,
            puzzle_2_example_answer=2713310158,
            puzzle_2_answer=29703395016,
        )

    def read(self, file_path: str) -> Tuple[Exchange]:
        with open(file_path, 'r') as f:
            exchange = Exchange()

            for monkey in f.read().split('\n\n'):
                (identifier, items, operator_type, operation_value, divisible_by, on_true, on_false) = \
                    re.search(
                        r".*(\d+):\n.*: (\d+(?:, \d+)*)\n.*old (.) (\d+|old)\n.*by (\d+)\n.*(\d+)\n.*(\d+)",
                        monkey,
                    ).groups()

                if operation_value == 'old':
                    if operator_type == '+':
                        operator_type = '*'
                        operation_value = 2
                    elif operator_type == '*':
                        operator_type = '**'
                        operation_value = 2
                    else:
                        raise RuntimeError(f'Unexpected operator type: {operator_type}')

                exchange.add_monkey(
                    identifier=int(identifier),
                    monkey=Monkey(
                        exchange=exchange,
                        identifier=int(identifier),
                        items=list(map(int, items.split(', '))),
                        operator_type=operator_type,
                        operation_value=int(operation_value),
                        divisible_by=int(divisible_by),
                        on_true=int(on_true),
                        on_false=int(on_false),
                    )
                )

        return exchange,

    def puzzle_1(self, exchange: Exchange) -> int:
        for _ in range(20):
            exchange.run_round_puzzle_1()

        inspection_count_ranking = sorted([monkey.number_of_inspected_items for monkey in exchange.monkeys.values()])
        return inspection_count_ranking[-2] * inspection_count_ranking[-1]

    def puzzle_2(self, exchange: Exchange) -> int:
        exchange.setup_round_2()

        for i in range(10000):
            exchange.run_round_puzzle_2()

        inspection_count_ranking = sorted([monkey.number_of_inspected_items for monkey in exchange.monkeys.values()])
        return inspection_count_ranking[-2] * inspection_count_ranking[-1]
