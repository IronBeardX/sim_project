# This file will contain a class for optimizing locally the parameters of the policy (s,S). Will use Hill Climbing

from simulation_engine import *
from sim_stats import SimStatistics
import numpy as np
import random as rnd
from scipy.optimize import minimize


class OptimizeSimulation:
    def __init__(
        self,
        simulation: InventorySimulation,
        initial_policy: tuple[int, int],
        runs: int,
        max_value: int,
    ) -> None:
        self.simulation: InventorySimulation = simulation
        self.initial_policy = initial_policy
        self.runs: int = runs
        if max_value < initial_policy[1]:
            raise Exception("The max_value variable must be greater than S")
        self.max_value: int = max_value

    def valid_point(self, s: int, S: int):
        return 0 <= s <= S <= self.max_value

    def fitness_function(self, s: int, S: int):
        """Returns the average fitness of several runs of the simulation"""
        self.simulation.s, self.simulation.S = s, S
        stats = SimStatistics(self.simulation)
        res = stats.calculate_statistics_results()
        return res.loss_expectation + res.costs_expectation

    def optimize(self, steps_search: int = 5, single_point: bool = False):
        sim = self.simulation
        policy = self.initial_policy
        actual_best = self.fitness_function(policy[0], policy[1])
        path = [policy]
        visited_points: set[(int, int)] = set()
        visited_points.add(policy)

        for i in range(steps_search):
            neighbors_fitness = []
            point = path[-1][0], path[-1][1]
            neighbors = (
                self.single_point_neighbors(point[0], point[1])
                if single_point
                else self.get_neighbors(point[0], point[1])
            )
            for n in neighbors:
                if n in visited_points:
                    continue
                neighbors_fitness.append((self.fitness_function(n[0], n[1]), n))
                visited_points.add(n)
            if len(neighbors_fitness) == 0:
                break
            best = min(neighbors_fitness, key=lambda x: x[0])
            if best[0] <= actual_best:
                actual_best = best[0]
                path.append(best[1])
        return path[-1]

    def get_neighbors(self, s: int, S: int) -> list[tuple[int, int]]:
        value = rnd.randint(1, 30)
        neighbors = [
            (s + value, S + value),
            (s - value, S - value),
            (s - value, S + value),
            (s + value, S - value),
        ]
        res_neighbors = [n for n in neighbors if self.valid_point(n[0], n[1])]
        return res_neighbors

    def single_point_neighbors(
        self, s: int, S: int, neighbor_count: int = 4
    ) -> list[tuple[int, int]]:
        neighbors: set[tuple[int, int]] = set()
        step_size = 30
        while len(neighbors) < neighbor_count:
            interpolator = rnd.random()
            value = int(min(step_size, s) * interpolator)
            neighbors.add((s - value, S))
            value = int(min(step_size, S - s) * interpolator)
            neighbors.add(((s + value), S))
        return list(neighbors)
