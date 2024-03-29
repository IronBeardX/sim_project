from sim_stats import SimStatistics
from registers import *
import matplotlib.pyplot as plt

class Graphics:
    def __init__(self, sim_statistics: SimStatistics) -> None:
        self.sim_stats: SimStatistics = sim_statistics

    def plot_sells(self):
        stats = self.sim_stats
        real_sales = stats.get_sells_data(lambda sell_list: sum([s.amount_seeled for s in sell_list]))
        plt.plot(real_sales[0], real_sales[1], label = 'real sales')
        plt.xlabel('Time')
        plt.ylabel('Total Sales')
        # plt.legend(handles = [real_sales], loc = 'upper right')
        plt.legend()
        plt.show()

    def plot_balance(self):
        stats = self.sim_stats
        balance = stats.get_balance_data(lambda balance: balance.balance)
        zero_line = [0 for b in balance[0]]
        plt.plot(balance[0], balance[1], label = 'balance of store')
        plt.plot(balance[0], zero_line, label = 'zero line', color = 'r')
        plt.xlabel('Time')
        plt.ylabel('Balance')
        plt.legend()
        plt.show()

    def plot_loss(self, product_price:float):
        stats = self.sim_stats
        loss = stats.get_sells_data(lambda sells: product_price * calculate_sell_loss(sells))
        plt.plot(loss[0], loss[1], label = 'money loss')
        plt.xlabel('Time')
        plt.ylabel('Total money loss')
        plt.legend()
        plt.show()


def calculate_sell_loss(sells:list[SellRecord]):
    demand = 0
    sold = 0
    for sell in sells:
        demand += sell.amount_asked
        sold += sell.amount_seeled
    return demand - sold