# This file will contain a class that will generate statistics from the Registry class of the simulation
import matplotlib.pyplot as plt
import numpy as np
from typing import Callable

from registers import *


class SimStatistics:
    """This class extracts statistics from a simulation"""
    def __init__(self, registry: Registry) -> None:
        self.flat_registry: FlattenRegistry = FlattenRegistry(registry)

    def give_fitness(self):
        """Fitness useful for optimization"""
        sells: list[tuple[int, list[SellRecord]]] = self.flat_registry.flat_sells
        hold_costs: list[tuple[int, PayHoldingRecord]] = self.flat_registry.flat_pay_holding
        buy_costs:list[tuple[int, BuyRecord]] = self.flat_registry.flat_buy

        total_loss = 0
        for _, sell in sells:
            loss = sum(map(lambda x: x.amount_asked - x.amount_seeled, sell))
            total_loss += loss
        total_hold_cost = sum(map(lambda t: t[1].cost, hold_costs))
        total_buy_cost = sum(map(lambda t: t[1].amount, buy_costs))
        return 3*total_loss + total_buy_cost + 2*total_hold_cost
    
    def get_sells_data(self, process_function:Callable[[list[SellRecord]], float]) -> tuple[list[int], list[float]]:
        """This function returns a tuple of 2 lists.
        The first list is a list of integers representing the time.
        The second list is a list of floats representing some processed value of the sells at that time.
        The 'process function' is a function that receives a list of SellsRecords and return some float representing statistic information of that list of sales
        """
        return SimStatistics.get_data(self.flat_registry.flat_sells, process_function)
    
    def get_buy_data(self, process_function: Callable[[BuyRecord], float]):
        """This function returns a tuple of 2 lists.
        The first list is a list of integers representing the time.
        The second list is a list of floats representing some processed value of the BuyRecord at that time.
        The 'process function' is a function that receives a single BuyRecord and return some float representing statistic information about it
        """
        return SimStatistics.get_data(self.flat_registry.flat_buy, process_function)
    
    def get_stock_data(self, process_function: Callable[[StockRecord], float]):
        """This function returns a tuple of 2 lists.
        The first list is a list of integers representing the time.
        The second list is a list of floats representing some processed value of the StockRecord at that time.
        The 'process function' is a function that receives a single StockRecord and return some float representing statistic information about it
        """
        return SimStatistics.get_data(self.flat_registry.flat_stock, process_function)
    
    def get_balance_data(self, process_function: Callable[[BalanceRecord], float]):
        """This function returns a tuple of 2 lists.
        The first list is a list of integers representing the time.
        The second list is a list of floats representing some processed value of the BalanceRecord at that time.
        The 'process function' is a function that receives a single BalanceRecord and return some float representing statistic information about it
        """
        return SimStatistics.get_data(self.flat_registry.flat_balance, process_function)
    
    def get_pay_hold_data(self, process_function: Callable[[PayHoldingRecord], float]):
        """This function returns a tuple of 2 lists.
        The first list is a list of integers representing the time.
        The second list is a list of floats representing some processed value of the PayHoldingRecord at that time.
        The 'process function' is a function that receives a single PayHoldingRecord and return some float representing statistic information about it
        """
        return SimStatistics.get_data(self.flat_registry.flat_pay_holding, process_function)

    @staticmethod
    def get_data[T](raw_data:list[tuple[int,T]], process_function:Callable[[T], float]) -> tuple[list[int], list[float]]:
        """This function returns a tuple of 2 lists.
        The first list is a list of integers representing the time.
        The second list is a list of floats representing some processed value of the elements of data in the raw_data input.
        The 'process_function' is a function that receives some value and computes some float representing statistic information about the value
        """
        time:list[int] = []
        values: list[float] = []
        
        for t, val in raw_data:
            time.append(t)
            values.append(process_function(val))
        return time, values


    # Plot the sells of the store along the time where it shows how much was asked and how much was seeled
    def plot_sells(self) -> None:
        sells: list[tuple[int, list[SellRecord]]] = self.flat_registry.flat_sells
        plot_data1 = []
        plot_data2 = []

        for time, sell_list in sells:
            demand = 0
            sold = 0
            print(len(sell_list))
            for sell in sell_list:
                demand += sell.amount_asked
                sold += sell.amount_seeled
            plot_data1.append((time, demand))
            plot_data2.append((time, sold))

        plt.plot(*zip(*plot_data1), label='Demand', color='b')
        plt.plot(*zip(*plot_data2), label='sold', color='g')
        plt.xlabel('Time')
        plt.ylabel('Amount')
        # plt.title('Sales vs Demand of the Store')
        plt.legend()

    def plot_stock(self) -> None:
        stock: list[tuple[int, StockRecord]] = self.flat_registry.flat_stock
        plot_data = []
        for time, stock_record in stock:
            plot_data.append((time, stock_record.amount))
        plt.plot(*zip(*plot_data), label='Stock', color='b')
        plt.xlabel('Time')
        plt.ylabel('Amount')
        # plt.title('Stock of the store')
        plt.legend()

    def plot_loss(self) -> None:
        sells: list[tuple[int, list[SellRecord]]] = self.flat_registry.flat_sells
        plot_data = []

        for time, sell_list in sells:
            demand = 0
            sold = 0
            for sell in sell_list:
                demand += sell.amount_asked
                sold += sell.amount_seeled
            plot_data.append((time, demand - sold))

        plt.plot(*zip(*plot_data), label='Loss', color='r')
        plt.xlabel('Time')
        plt.ylabel('Amount')
        # plt.title('Loss of the store')
        plt.legend()

    def plot_holding_costs(self) -> None:
        pay_holding: list[tuple[int, PayHoldingRecord]] = self.flat_registry.flat_pay_holding
        plot_data = []
        for time, pay_holding_record in pay_holding:
            plot_data.append((time, pay_holding_record.cost))
        plt.plot(*zip(*plot_data), label='Holding Cost', color='r')
        plt.xlabel('Time')
        plt.ylabel('Amount')
        # plt.title('Holding Cost of the store')
        plt.legend()

    def plot_buy(self) -> None:
        buy: list[tuple[int, BuyRecord]] = self.flat_registry.flat_buy
        plot_data = []
        for time, buy_record in buy:
            plot_data.append((time, buy_record.amount))
        plt.plot(*zip(*plot_data), label='Buy', color='g')
        plt.xlabel('Time')
        plt.ylabel('Amount')
        # plt.title('Buy of the store')
        plt.legend()

    def plot_bar_sell(self) -> None:
        sells: list[tuple[int, list[SellRecord]]] = self.flat_registry.flat_sells
        for time, sell_list in sells:
            amount_asked = 0
            amount_seeled = 0
            for sell in sell_list:
                amount_asked += sell.amount_asked
                amount_seeled += sell.amount_seeled
            plt.bar(time, amount_asked, color='r')
            plt.bar(time, amount_seeled, color='b')
        plt.xlabel('Time')
        plt.ylabel('Amount')
        plt.title('Sales of the store')
        plt.show()

    def plot_balance(self) -> None:
        balance: list[tuple[int, BalanceRecord]] = self.flat_registry.flat_balance
        plot_data = []
        for time, balance_record in balance:
            plot_data.append((time, balance_record.balance))
        # plt.plot(*zip(*plot_data), label='Balance', color='b')
        # Dividing data in two parts, ones with positive balance and other with negative balance
        positive_data = [(time, balance) for time, balance in plot_data if balance > 0]
        negative_data = [(time, -balance) for time, balance in plot_data if balance < 0]
        plt.plot(*zip(*positive_data), label='Positive Balance', color='g')
        plt.plot(*zip(*negative_data), label='Negative Balance', color='r')
        plt.xlabel('Time')
        plt.ylabel('Amount')
        # plt.title('Balance of the store')
        plt.legend()


class FlattenRegistry:
    def __init__(self, registry: Registry) -> None:
        self.registry: Registry = registry
        self.flat_sells: list[tuple[int, list[SellRecord]]] = self.flat_sells_registry()
        self.flat_stock: list[tuple[int, StockRecord]] = self.flat_stock_registry()
        self.flat_buy: list[tuple[int, BuyRecord]] = self.flat_buy_registry()
        self.flat_balance: list[tuple[int, BalanceRecord]] = self.flat_balance_registry()
        self.flat_pay_holding: list[tuple[int, PayHoldingRecord]] = self.flat_pay_holding_registry()

    def flat_sells_registry(self) -> list[tuple[int, list[SellRecord]]]:
        """Returns a sorted list of tuples where the first element is the time in which a sell
        occurs and the second one is a list of sells at that time"""
        sells: list[tuple[int, list[SellRecord]]] = sorted(
            self.registry.sell_registry.items()
        )
        return sells

    def flat_stock_registry(self) -> list[tuple[int, StockRecord]]:
        """Returns a sorted list of tuples where the first element is the time and the second one
        is a StockRecord"""
        stock: list[tuple[int, StockRecord]] = sorted(
            self.registry.stock_registry.items()
        )
        return stock

    def flat_buy_registry(self) -> list[tuple[int, BuyRecord]]:
        """Returns a sorted list of tuples where the first element is the time and the second one
        is the BuyRecord"""
        buy: list[tuple[int, BuyRecord]] = sorted(
            self.registry.buy_registry.items())
        return buy

    def flat_balance_registry(self) -> list[tuple[int, BalanceRecord]]:
        """Returns a sorted list of tuples where the first element is the time and the second one
        is a BalanceRecord"""
        balance: list[tuple[int, BalanceRecord]] = sorted(
            self.registry.balance_registry.items()
        )
        return balance

    def flat_pay_holding_registry(self) -> list[tuple[int, PayHoldingRecord]]:
        """Returns a sorted list of tuples where the first element is the time and the second one
        is a PayHoldRecord"""
        pay_holding: list[tuple[int, PayHoldingRecord]] = sorted(
            self.registry.pay_holding_registry.items()
        )
        return pay_holding
