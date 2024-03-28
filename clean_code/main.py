from simulation_engine import *
from sim_stats import FlattenRegistry, SimStatistics
import matplotlib.pyplot as plt
simulation_time:int = 24 * 60 # 14 hours * 60 min = 840
# The simulation time is in minutes
sim = InventorySimulation(sim_duration=simulation_time, s=10, S= 200)
sim.run()

sim_statistics = SimStatistics(sim.registry)
# plotting the seels of the store
plt.figure(figsize=(12, 20))
plt.title('Simulation Statistics')
# plt.subplot(3, 1, 1)
sim_statistics.plot_sells()
# sim_statistics.plot_loss()
plt.show()
plt.figure(figsize=(12, 20))
plt.title('Simulation Statistics')
# plt.subplot(3, 1, 2)
# sim_statistics.plot_stock()
sim_statistics.plot_buy()
plt.show()
plt.figure(figsize=(12, 20))
plt.title('Simulation Statistics')
# plt.subplot(3, 1, 3)
sim_statistics.plot_holding_costs()
plt.show()