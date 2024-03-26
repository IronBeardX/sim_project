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
                sim_duration:int=200, 
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

        # Variables for storing statistical information
        self.st_inventory_level_records = [] # Records of the inventory levels for each event
        self.st_holding_payment_records = [] # Records of the holding costs for each event
        self.st_lost_sale_records = [] # Records of the lost sales for each event
        self.st_order_records = [] # Records of the orders for each event
        self.st_order_payment_records = [] # Records of the ordering costs for each event
        self.st_balance_records = [] # Records of the balance for each event
        self.st_earning_records = [] # Records of the earnings for each event
        self.st_sell_records = [] # Records of the sells for each event

    #[x]
    def demand_event_snapshot(self, sold_product:int, gain:int, lost_sale:int):
        # A snapshot of the necesary information on a demand event
        self.st_earning_records.append((self.time, gain))
        self.st_sell_records.append((self.time, sold_product))
        self.st_balance_records.append((self.time, self.balance))# [ ] if Two events happen at the same time it will be a problem
        self.st_inventory_level_records.append((self.time, self.inventory_level))
        self.st_lost_sale_records.append((self.time, lost_sale))

    #[x]
    def order_event_snapshot(self, order:int):
        # A snapshot of the necesary information on a order event
        self.st_order_records.append((self.time, order))
        self.st_order_payment_records.append((self.time, self.ordering_cost_func(order)))
        self.st_inventory_level_records.append((self.time, self.inventory_level))
        self.st_balance_records.append((self.time, self.balance))# [ ] if Two events happen at the same time it will be a problem


    #[x]
    def initialize_simulation(self):
        self.time = 0
        self.pending_orders = []
        self.balance = self.initial_balance
        self.total_lost_sales = 0
        self.inventory_level = self.initial_inventory_level

        # Initializing statistical records
        self.st_inventory_level_records = []
        self.st_holding_payment_records = []
        self.st_lost_sale_records = []
        self.st_order_records = []
        self.st_balance_records = []
        self.st_earning_records = []
        self.st_sell_records = []
        self.st_order_payment_records = []

    #[x] missing demand randomization information
    def generate_client_arrival(self):
        # Generate customer demand according to a specified distribution
        arrival_time, demand = self.clients_arrival_dist(), self.client_demand_dist()
        if self.time + arrival_time > self.sim_duration:
            return None, None
        return self.time + arrival_time, demand

    #[x]
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

    #[x]
    def calculate_holding_costs(self, interval_time:int):
        # Calculate holding costs and holding costs incurred during the simulation
        self.balance -= (self.holding_cost_rate * self.inventory_level) * interval_time
        self.st_holding_payment_records.append((self.time, (self.holding_cost_rate * self.inventory_level) * interval_time))

    #[x]
    def fulfill_demand(self, demand:int):
        # Fulfill customer demand based on available inventory
        gain = 0
        lost_sale = 0
        if self.inventory_level >= demand:
            self.inventory_level -= demand
            sold_product, gain = demand, demand * self.product_value
            self.balance += gain
        else:
            lost_sale = demand - self.inventory_level
            self.inventory_level = 0
            self.total_lost_sales += lost_sale * self.product_value
            sold_product, gain = demand - lost_sale, (demand - lost_sale) * self.product_value
            self.balance += gain
        
        self.demand_event_snapshot(sold_product, gain, lost_sale)

        return self.generate_client_arrival()
    
    #[x]
    def simulate_order_delivery(self, order_amount:int):
        # Simulate order delivery lead times and update inventory levels accordingly
        self.inventory_level += order_amount
        self.balance -= self.ordering_cost_func(order_amount)
        self.pending_orders.remove(order_amount)

        self.order_event_snapshot(order_amount)

    #[x]
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
        heapq.heappush(event_queue, (self.sim_duration + 1, None, 'ending_simulation'))

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
                if next_client:
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


    #[ ]
    def plot_results(self):
        # Plot results of the simulation
        # Plot results of the simulation
        plt.figure(figsize=(12, 6))

        plt.subplot(2, 1, 1)
        plt.plot(range(len(self.st_inventory_level_records)), self.st_inventory_level_records, label='Inventory Level')
        plt.xlabel('Time')
        plt.ylabel('Inventory Level')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(range(len(self.st_holding_payment_records)), self.st_holding_payment_records, label='Holding Costs')
        plt.xlabel('Time')
        plt.ylabel('Holding Costs')
        plt.legend()

        plt.tight_layout()
        plt.show()

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
