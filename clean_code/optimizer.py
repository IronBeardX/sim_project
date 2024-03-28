# This file will contain a class for optimizing locally the parameters of the policy (s,S). Will use Hill Climbing

from simulation_engine import *
import numpy as np
from scipy.optimize import minimize

class OptimizeSimulation:
    def __init__(self, simulation: InventorySimulation, runs:int) -> None:
        self.simulation = simulation
        self.runs = runs

    def optimize(self):
        pass
