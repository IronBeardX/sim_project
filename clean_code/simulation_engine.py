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
        client_arrival_dist: Callable[[],int] = poisson_random_variable(5),
        client_demand_dist: Callable = random.randint(1, 10),
        sim_duration:int = 840 # 14 hours -> 14 * 60min = 840min
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
        """This is the time difference between payments for holding the inventory"""
        self.product_value: int = product_value
        # ------ Variables that represents the distributions
        self.client_arrival_dist: Callable[[],int] = client_arrival_dist
        self.client_demand_dist: Callable[[],int] = client_demand_dist
        self.registry: Registry = Registry()
        # ------ Now are the variables of the state of the simulation -------
        self.time:int = 0
        """This is the actual simulation time"""
        self.sim_duration:int = sim_duration
        """The duration of a single simulation"""
        self.actual_balance: int = 0
        """This is the actual balance of the store account in the """
        self.initial_inventory_level:int = initial_inventory_level
        self.actual_inventory_level: int = initial_inventory_level
        self.pending_order: bool = False
        # -------- Simulation queue --------
        self.event_queue:list[Event] = []
        """The priority queue of events"""

    def initialize(self):
        """Initialize some events for the simulation"""
        self.event_queue = []
        heapq.heapify(self.event_queue)
        self.time = 0
        self.actual_balance = 0
        self.actual_inventory_level = self.initial_inventory_level
        self.pending_order = False
        self.registry = Registry()
        self.verify_supply_policy()
        self.generate_client_arrival_event()
        self.add_simulation_end_event()

    def generate_client_arrival_event(self):
        """Generate a new Sell Event and push it to the queue"""
        time:int = self.client_arrival_dist()
        amount:int = self.client_demand_dist()
        client_event:SellEvent = SellEvent(self.time + time, amount)
        self.add_to_event_queue(client_event)

    def verify_supply_policy(self):
        """This function verifies if it is time for ask more supplies"""
        if self.actual_inventory_level > self.s or self.pending_order:
            return
        amount = self.S - self.actual_inventory_level
        time = self.time + self.lead_time
        event = SupplyArrivalEvent(time, amount)
        self.add_to_event_queue(event)
        self.pending_order = True

    def add_simulation_end_event(self):
        end:SimulationEndEvent = SimulationEndEvent(self.sim_duration)
        self.add_to_event_queue(end)

    def generate_pay_holding_event(self):
        pay_hold_event:PayHoldingEvent = PayHoldingEvent(self.time + self.holding_pay_time)
        self.add_to_event_queue(pay_hold_event)

    def add_to_event_queue(self, event:Event):
        """Adds an event to the simulation queue"""
        heapq.heappush(self.event_queue, event)

    def get_next_event_in_queue(self) -> Event:
        """Extracts the next event in the queue"""
        event:Event = heapq.heappop(self.event_queue)
        return event
    
    def process_sell_event(self):
        pass

    def process_supply_arrival_event(self):
        pass

    def process_pay_holding_event(self):
        pass

    def process_simulation_end(self):
        pass
    
    def step(self):
        """Extracts the next event in the Event Queue and process it"""
        event: Event = self.get_next_event_in_queue()
        time = event.time
        self.time = time # Advance the simulation time to the Event time
        

    def run(self):
        """Run the simulation"""
        self.initialize()
        

