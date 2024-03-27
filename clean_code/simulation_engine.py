import random
from typing import Callable
import heapq

from clean_code.registers import *
from clean_code.events import *
from utils import poisson_random_variable


class InventorySimulation:
    def __init__(
        self,
        s: int = 10,
        S: int = 20,
        initial_inventory_level: int = 0,
        ordering_cost_function: Callable[[int], int] = lambda x: x * 10,
        lead_time: int = 10,
        holding_cost_rate: int = 3,  # The pay constant for holding inventory
        holding_pay_time: int = 60,  # 60 minutes, 1 hour. After that time the store must pay for the inventory
        product_value: int = 10,
        client_arrival_dist: Callable = poisson_random_variable(5),
        client_demand_dist: Callable = random.randint(1, 10),
    ):
        if (s >= S):
            raise Exception('Problem: s >= S and this should not happen')
        self.s: int = s
        """The minimum amount of units in inventory before ask for supply"""
        self.S: int = S
        """The maximum amount of units the store wants to have in stock"""
        self.ordering_cost_func: Callable[[int], int] = ordering_cost_function
        self.lead_time: int = lead_time
        """The time for the productos of supplier arrive"""
        self.holding_cost_rate: int = holding_cost_rate
        self.holding_pay_time: int = holding_pay_time
        self.product_value: int = product_value
        # ------ Variables that represents the distributions
        self.client_arrival_dist: Callable = client_arrival_dist
        self.client_demand_dist: Callable = client_demand_dist
        self.registry = Registry()
        # ------ Now are the variables of the state of the simulation -------
        self.time:int = 0
        """This is the actual simulation time"""
        self.actual_balance: int = 0
        """This is the actual balance of the store account in the """
        self.actual_inventory_level: int = initial_inventory_level
        self.pending_order: bool = False
        # -------- Simulation queue --------
        self.event_queue = []
        heapq.heapify(self.event_queue)

    def verify_supply_policy(self):
        if self.actual_inventory_level > self.s:
            return
        amount = self.S - self.actual_inventory_level
        time = self.time + self.lead_time
        event = SupplyArrivalEvent(time, amount)
        self.add_to_event_queue(event)

    def add_to_event_queue(self, event:Event):
        heapq.heappush(self.event_queue, event)

    def get_next_event_in_queue(self) -> Event:
        event:Event = heapq.heappop(self.event_queue)
        return event

    def initialize(self):
        """Initialize some events for the simulation"""

        pass

    def run(self):
        """Run the simulation"""
        pass

