# This file will contain a class that will generate statistics from the Registry class of the simulation
import matplotlib.pyplot as plt
import numpy as np

from registers import *


class SimStatistics:
    def __init__(self, registry: Registry) -> None:
        self.flat_registry: FlattenRegistry = FlattenRegistry(registry)

    # Plot the sells of the store along the time where it shows how much was asked and how much was seeled
    def plot_sells(self) -> None:
        sells = self.flat_registry.flat_sells
        for time, sell_list in sells:
            amount_asked = 0
            amount_seeled = 0
            for sell in sell_list:
                amount_asked += sell.amount_asked
                amount_seeled += sell.amount_seeled
            plt.plot(time, amount_asked, 'ro')
            plt.plot(time, amount_seeled, 'bo')
        plt.xlabel('Time')
        plt.ylabel('Amount')
        plt.title('Sells of the store')
        plt.show()


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
