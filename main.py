# Import necessary libraries
from typing import Callable
from utils import poisson_random_variable

import numpy as np  # For random number generation
import matplotlib.pyplot as plt  # For plotting results
import random # For random number generation
import heapq

# Define class for inventory system simulation
class InventorySimulation:
    def __init__(self, 
                s:int = 10,
                S:int = 20,
                holding_cost_rate:int = 3, 
                lead_time:int = 10, 
                sim_duration:int=1000, 
                initial_balance:int=100,
                product_value:int = 10,
                initial_inventory_level:int= 0,
                ordering_cost_func:Callable = lambda x: x * 10, 
                clients_arrival_dist:Callable = lambda: poisson_random_variable(5), 
                client_attention_dist:Callable = lambda: random.randint(1, 10),
                client_demand_dist:Callable = lambda: random.randint(1, 10)
                ):
        # Initialize simulation parameters
        self.s = s  # Reorder point
        self.S = S  # Order-up-to level
        self.ordering_cost_func = ordering_cost_func  # Function to calculate ordering costs
        self.holding_cost_rate = holding_cost_rate  # Holding cost per unit per time period
        self.lead_time = lead_time  # Lead time for order delivery
        self.initial_inventory_level = initial_inventory_level  # Initial inventory level
        self.inventory_level = initial_inventory_level  # Current inventory level
        self.pending_orders = []  # Pending orders
        self.total_lost_sales = 0  # Total lost sales due to stockouts
        self.time = 0  # Simulation time
        self.sim_duration = sim_duration  # Total simulation duration
        self.product_value = product_value  # Value of the product
        self.initial_balance = initial_balance
        self.balance = initial_balance

        self.clients_arrival_dist = clients_arrival_dist # Distribution of customer arrivals
        self.client_attention_dist = client_attention_dist # Distribution of customer attention
        self.client_demand_dist = client_demand_dist # Distribution of the amount of the customer demand

    #[x] missing initializing statistical stuff
    def initialize_simulation(self):
        self.time = 0
        self.pending_orders = []
        self.balance = self.initial_balance
        self.total_lost_sales = 0
        self.inventory_level = self.initial_inventory_level

    #[x] missing demand randomization information and statistical stuff
    def generate_client_arrival(self):
        # Generate customer demand according to a specified distribution
        arrival_time, demand = self.clients_arrival_dist(), self.client_demand_dist()
        if self.time + arrival_time > self.sim_duration:
            return None, None
        return self.time + arrival_time, demand

    #[x] missing statistical stuff 
    def place_order(self):
        # Determine when to place orders based on the (s, S) policy
        if self.inventory_level <= self.s - sum(self.pending_orders):
            order_quantity = self.S - self.inventory_level - sum(self.pending_orders)
            if order_quantity <= 0:
                return None, None
            if self.time + self.lead_time >= self.sim_duration:
                return None, None
            self.pending_orders.append(order_quantity)
            return self.time + self.lead_time, order_quantity
        return None, None

    #[x] missing statistical stuff
    def calculate_holding_costs(self, interval_time:int):
        # Calculate holding costs and holding costs incurred during the simulation
        self.balance -= (self.holding_cost_rate * self.inventory_level) * interval_time

    #[x] missing statistical stuff
    def fulfill_demand(self, demand:int):
        # Fulfill customer demand based on available inventory
        if self.inventory_level >= demand:
            self.inventory_level -= demand
            self.balance += demand * self.product_value
        else:
            remaining_demand = demand - self.inventory_level
            self.inventory_level = 0
            self.total_lost_sales += remaining_demand * self.product_value
            self.balance += (demand - remaining_demand) * self.product_value
        return self.generate_client_arrival()
    
    #[x] missing statistical stuff
    def simulate_order_delivery(self, order_amount:int):
        # Simulate order delivery lead times and update inventory levels accordingly
        self.inventory_level += order_amount
        self.balance -= self.ordering_cost_func(order_amount)
        self.pending_orders.remove(order_amount)

    #[x] missing statistical stuff
    def run_simulation(self):
        # Creating a priority queue for events
        event_queue = []
        heapq.heapify(event_queue)

        # Initialize simulation setting all values to default
        self.initialize_simulation()

        # Generate the first event as a customer demand
        first_customer, demand = self.generate_client_arrival()

        # Generate the first provider order if needed
        first_order, amount = self.place_order()

        heapq.heappush(event_queue, (first_customer, demand, 'demand'))
        if first_order:
            heapq.heappush(event_queue, (first_order, amount, 'order_arrival'))
        
        # Adding the the final event
        heapq.heappush(event_queue, (self.sim_duration, None, 'ending_simulation'))

        while event_queue:
            # Get the next event
            event = heapq.heappop(event_queue)

            # Move time to the event time
            interval_time = event[0] - self.time
            self.time = event[0]

            # Calculate inventory costs
            self.calculate_holding_costs(interval_time)

            if not event:
                # If there are no more events, break the loop
                break

            if event[2] == 'demand':
                # Demand event
                # Fullfill the demand substracting from current inventory [x]
                # Generate a new client arrival [x]
                # Record the sale [ ]
                # Generate a provider order if necesary [x]
                next_client, demand = self.fulfill_demand(event[1])
                if not next_client:
                    heapq.heappush(event_queue, (next_client, demand, 'demand'))
                next_order, amount = self.place_order()
                if next_order:
                    heapq.heappush(event_queue, (next_order, amount, 'order_arrival'))

            elif event[2] == 'order_arrival':
                # Order arrival event
                # Update inventory levels
                # Generate a new provider order if necesary
                self.simulate_order_delivery(event[1])
                next_order, amount = self.place_order()
                if next_order:
                    heapq.heappush(event_queue, (next_order, amount, 'order_arrival'))

            elif event[2] == 'ending_simulation':
                # Ending simulation event
                break

            else:
                raise ValueError('Invalid event type')

    #[ ] Add statistical information needed in previous methods
    def plot_results(self):
        # Plot results of the simulation
        pass

# Main function
def main():
    # Initialize simulation
    simulation = InventorySimulation(
        initial_inventory_level=15,
    )

    simulation.run_simulation()

    # Plot results
    simulation.plot_results()

# Run main function
if __name__ == "__main__":
    main()
    # testing_heapq()
