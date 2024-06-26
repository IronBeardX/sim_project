from sim_stats import SimStatistics, calculate_sell_loss
from registers import *
import matplotlib.pyplot as plt


class Graphics:
    def __init__(self, sim_statistics: SimStatistics) -> None:
        self.sim_stats: SimStatistics = sim_statistics

    def plot_sells(self):
        stats = self.sim_stats
        real_sales = stats.get_sells_data(
            lambda sell_list: sum([s.amount_seeled for s in sell_list])
        )
        plt.plot(real_sales[0], real_sales[1], label="real sales")
        plt.xlabel("Time")
        plt.ylabel("Total Sales")
        # plt.legend(handles = [real_sales], loc = 'upper right')
        plt.legend()
        plt.show()

    def plot_balance(self):
        stats = self.sim_stats
        balance = stats.get_balance_data(lambda balance: balance.balance)
        zero_line = [0 for b in balance[0]]
        plt.plot(balance[0], balance[1], label="balance of store")
        plt.plot(balance[0], zero_line, label="zero line", color="r")
        plt.xlabel("Time")
        plt.ylabel("Balance")
        plt.legend()
        plt.show()

    def plot_loss(self, product_price: float):
        stats = self.sim_stats
        loss = stats.get_sells_data(
            lambda sells: product_price * calculate_sell_loss(sells)
        )
        plt.plot(loss[0], loss[1], label="money loss in sales")
        plt.xlabel("Time")
        plt.ylabel("Total money loss")
        plt.legend()
        plt.show()

    def plot_inventory_holding_cost(self):
        stats = self.sim_stats
        costs = stats.get_pay_hold_data(lambda pay_record: pay_record.cost)
        plt.plot(costs[0], costs[1], label="holding costs")
        plt.xlabel("Time")
        plt.ylabel("Total money spent")
        plt.legend()
        plt.show()

    def plot_supply_costs(self):
        stats = self.sim_stats
        supply_costs = stats.get_buy_data(lambda buy_record: buy_record.cost)
        plt.plot(supply_costs[0], supply_costs[1], label="supply costs")
        plt.xlabel("Time")
        plt.ylabel("Money spent in supply payment")
        plt.legend()
        plt.show()
