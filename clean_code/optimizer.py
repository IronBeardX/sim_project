# This file will contain a class for optimizing locally the parameters of the policy (s,S). Will use Hill Climbing

from simulation_engine import *
from sim_stats import SimStatistics
import numpy as np
import random as rnd
from scipy.optimize import minimize

class OptimizeSimulation:
    def __init__(self, simulation: InventorySimulation, runs: int) -> None:
        self.simulation = simulation
        self.runs = runs

    @staticmethod
    def valid_point(s: int, S: int):
        return s >= 0 and s <= S

    def fitness_function(self, s: int, S: int):
        """Returns the average fitness of several runs of the simulation"""
        results = []
        for _ in range(self.runs):
            self.simulation.run_with(s, S)
            stats = SimStatistics(self.simulation.registry)
            cost = stats.give_fitness()
            results.append(cost)
        return np.mean(results)

    def optimize(self, steps_search:int = 5):
        sim = self.simulation
        policy = (sim.s,sim.S)
        actual_best = self.fitness_function(policy[0], policy[1])
        path = [policy]
        visited_points:set[(int,int)] = set()
        visited_points.add(policy)
        
        for i in range(steps_search):
            neighbors_fitness = []
            for n in self.get_neighbors(path[-1][0], path[-1][1]):
                if n in visited_points:
                    continue
                neighbors_fitness.append((self.fitness_function(n[0], n[1]), n))
                visited_points.add(n)
            if len(neighbors_fitness) == 0:
                break
            best = max(neighbors_fitness, key=lambda x: x[0])
            if best[0] >= actual_best:
                actual_best = best[0]
                path.append(best[1])
        return path[-1]

    def get_neighbors(self, s: int, S: int) -> list[tuple[int, int]]:
        value = rnd.randint(1,30)
        neighbors = [(s + value, S + value), (s - value, S - value), (s - value, S + value), (s + value, S - value)]
        res_neighbors = [
            n for n in neighbors if OptimizeSimulation.valid_point(n[0], n[1])
        ]
        return res_neighbors
