import dataclasses
from typing import Tuple, List, Dict
from advent_of_code.abstract_puzzles import AbstractPuzzles
import re
import numpy as np


@dataclasses.dataclass
class Robot:
    ore_cost: int = 0
    clay_cost: int = 0
    obsidian_cost: int = 0


@dataclasses.dataclass
class Blueprint:
    ore_robot: Robot
    clay_robot: Robot
    obsidian_robot: Robot
    geode_robot: Robot


DATA_TYPE = List[Blueprint]


class Puzzles(AbstractPuzzles):
    def __init__(self, method_name):
        super().__init__(
            method_name,
            day=19,
            puzzle_1_example_answer=33,
            puzzle_1_answer=988,
            puzzle_2_example_answer=56*62,
            puzzle_2_answer=None,
        )

    def read(self, file_path: str) -> Tuple[DATA_TYPE]:
        data = []

        with open(file_path, 'r') as f:
            for line in f.read().splitlines():
                matches = re.match(r".*Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.", line).groups()

                data.append(Blueprint(
                    ore_robot=Robot(ore_cost=int(matches[0])),
                    clay_robot=Robot(ore_cost=int(matches[1])),
                    obsidian_robot=Robot(ore_cost=int(matches[2]), clay_cost=int(matches[3])),
                    geode_robot=Robot(ore_cost=int(matches[4]), obsidian_cost=int(matches[5])),
                ))

        return data,

    def test_puzzle_1_example(self):
        return

    def test_puzzle_1(self):
        return

    # def test_puzzle_2(self):
    #     return

    def test_puzzle_2_example(self):
        return

    def puzzle_1(self, blueprints: DATA_TYPE) -> int:
        quality_levels = []

        for blueprint_id, blueprint in enumerate(blueprints, 1):
            print(blueprint_id)
            geodes = maximize_geodes(
                blueprint,
                ore_robots=1,
                clay_robots=0,
                obsidian_robots=0,
                geode_robots=0,
                ores=0,
                clay=0,
                obsidian=0,
                geodes=0,
                time_remaining=24,
                memo={},
            )
            quality_levels.append(blueprint_id * geodes)

        return sum(quality_levels)

    def puzzle_2(self, blueprints: DATA_TYPE) -> int:
        quality_levels = 1

        for blueprint_id, blueprint in enumerate(blueprints[:3], 1):

            geodes = maximize_geodes(
                blueprint,
                ore_robots=1,
                clay_robots=0,
                obsidian_robots=0,
                geode_robots=0,
                ores=0,
                clay=0,
                obsidian=0,
                geodes=0,
                time_remaining=32,
                memo={},
            )
            print(blueprint_id, geodes)
            quality_levels *= geodes
            # quality_levels.append(blueprint_id * geodes)

        return quality_levels


def maximize_geodes2(blueprint: Blueprint, ore_robots: int, clay_robots: int, obsidian_robots: int, geode_robots: int, ores: int, clay: int, obsidian: int, geodes: int, time_remaining: int) -> int:
    number_of_robots = np.arange(1, 25)
    storage = (np.cumsum(np.triu(np.ones((24, 24), dtype=int)), axis=1).T * number_of_robots).T
    production = np.triu((np.array([np.arange(24, 0, -1)] * 24).T * number_of_robots).T)

    ore_robot_ore_costs = (number_of_robots - 1) * blueprint.ore_robot.ore_cost
    clay_robot_ore_costs = number_of_robots * blueprint.clay_robot.ore_cost
    obsidian_robot_ore_costs = number_of_robots * blueprint.obsidian_robot.ore_cost
    obsidian_robot_clay_costs = number_of_robots * blueprint.obsidian_robot.clay_cost
    geode_robot_ore_costs = number_of_robots * blueprint.geode_robot.ore_cost
    geode_robot_obsidian_costs = number_of_robots * blueprint.geode_robot.obsidian_cost

    # ores = (production.T - ore_robot_ore_costs).T
    # clay = (production.T - clay_robots_ore_costs).T

    ores = (production.T - geode_robot_ore_costs).T
    obsidian = production

    # Requirements
    has_enough_obsidian_for_geode_robot = (storage.T >= geode_robot_obsidian_costs).T


    return 0


def maximize_geodes(
        blueprint: Blueprint,
        ore_robots: int,
        clay_robots: int,
        obsidian_robots: int,
        geode_robots: int,
        ores: int,
        clay: int,
        obsidian: int,
        geodes: int,
        time_remaining: int,
        memo: Dict[str, int],
) -> int:
    if time_remaining == 0:
        return geodes

    max_geodes = []

    # tag = f"{ore_robots}-{clay_robots}-{obsidian_robots}-{geode_robots}-{ores}-{clay}-{obsidian}-{geodes}-{time_remaining}"
    tag = f"{ores + ore_robots * time_remaining}-{clay + clay_robots * time_remaining}-{obsidian + obsidian_robots * time_remaining}-{geodes + geode_robots * time_remaining}-{time_remaining}"
    # tag = f"{ore_robots}-{clay_robots}-{obsidian_robots}-{geode_robots}-{geodes}-{time_remaining}"
    if tag in memo:
        return memo[tag]

    max_ore_robots = max(
        blueprint.ore_robot.ore_cost,
        blueprint.clay_robot.ore_cost,
        blueprint.obsidian_robot.ore_cost,
        blueprint.geode_robot.ore_cost,
    )
    max_ores_necessary = max_ore_robots * time_remaining

    max_clay_robots = max(
        blueprint.ore_robot.clay_cost,
        blueprint.clay_robot.clay_cost,
        blueprint.obsidian_robot.clay_cost,
        blueprint.geode_robot.clay_cost,
    )
    max_clay_necessary = max_clay_robots * time_remaining

    max_obsidian_robots = max(
        blueprint.ore_robot.obsidian_cost,
        blueprint.clay_robot.obsidian_cost,
        blueprint.obsidian_robot.obsidian_cost,
        blueprint.geode_robot.obsidian_cost,
    )
    max_obsidian_necessary = max_obsidian_robots * time_remaining

    if ores >= blueprint.geode_robot.ore_cost and obsidian >= blueprint.geode_robot.obsidian_cost:
        max_geodes.append(maximize_geodes(
            blueprint,
            ore_robots,
            clay_robots,
            obsidian_robots,
            geode_robots + 1,
            ores - blueprint.geode_robot.ore_cost + ore_robots,
            clay + clay_robots,
            obsidian - blueprint.geode_robot.obsidian_cost + obsidian_robots,
            geodes + geode_robots,
            time_remaining - 1,
            memo
        ))

    if obsidian + obsidian_robots * time_remaining < max_obsidian_necessary and obsidian_robots < max_obsidian_robots and ores >= blueprint.obsidian_robot.ore_cost and clay >= blueprint.obsidian_robot.clay_cost:
        max_geodes.append(maximize_geodes(
            blueprint,
            ore_robots,
            clay_robots,
            obsidian_robots + 1,
            geode_robots,
            ores - blueprint.obsidian_robot.ore_cost + ore_robots,
            clay - blueprint.obsidian_robot.clay_cost + clay_robots,
            obsidian + obsidian_robots,
            geodes + geode_robots,
            time_remaining - 1,
            memo
        ))

    if clay + clay_robots * time_remaining < max_clay_necessary and clay_robots < max_clay_robots and ores >= blueprint.clay_robot.ore_cost:
        max_geodes.append(maximize_geodes(
            blueprint,
            ore_robots,
            clay_robots + 1,
            obsidian_robots,
            geode_robots,
            ores - blueprint.clay_robot.ore_cost + ore_robots,
            clay + clay_robots,
            obsidian + obsidian_robots,
            geodes + geode_robots,
            time_remaining - 1,
            memo
        ))

    if ores + ore_robots * time_remaining < max_ores_necessary and ore_robots < max_ore_robots and ores >= blueprint.ore_robot.ore_cost:
        max_geodes.append(maximize_geodes(
            blueprint,
            ore_robots + 1,
            clay_robots,
            obsidian_robots,
            geode_robots,
            ores - blueprint.ore_robot.ore_cost + ore_robots,
            clay + clay_robots,
            obsidian + obsidian_robots,
            geodes + geode_robots,
            time_remaining - 1,
            memo
        ))

    max_geodes.append(maximize_geodes(
        blueprint,
        ore_robots,
        clay_robots,
        obsidian_robots,
        geode_robots,
        ores + ore_robots,
        clay + clay_robots,
        obsidian + obsidian_robots,
        geodes + geode_robots,
        time_remaining - 1,
        memo
    ))

    result = max(max_geodes)
    memo[tag] = result

    return result
