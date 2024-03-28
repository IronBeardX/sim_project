from simulation_engine import *
from sim_stats import FlattenRegistry, SimStatistics

simulation_time:int = 14 * 60 # 14 hours * 60 min = 840
# The simulation time is in minutes
sim = InventorySimulation(sim_duration=simulation_time, s=10, S= 200)
sim.run()

sim_statistics = SimStatistics(sim.registry)
# plotting the seels of the store
sim_statistics.plot_bar_sell()