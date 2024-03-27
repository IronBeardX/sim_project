
class Registry:
    """This is the class for store useful information of the simulation"""
    def __init__(self) -> None:
        self.sell_registry:dict[int,]


class Record:
    """Base class for all the information records of the simulation"""
    def __init__(self, time:int = 0) -> None:
        self.time = time

class SellRecord(Record):
    """This record store information about the sell of products at a time"""
    def __init__(self, time: int, amount_asked:int, amount_seeled:int) -> None:
        super().__init__(time)
        self.amount_asked:int = amount_asked
        """The units that the client asked to buy"""
        self.amount_seeled:int = amount_seeled
        """The number of units that the store could sell to the client"""

class StockRecord(Record):
    """This record store the information of the number of units of the product in storage at a time"""
    def __init__(self, time: int, amount:int) -> None:
        super().__init__(time)
        self.amount:int = amount
        """The number of units of the product that are available in the store"""

class BuyRecord(Record):
    """This record store the information of the number of units bought to the provider at a point in time"""
    def __init__(self, time: int, amount:int) -> None:
        super().__init__(time)
        self.amount:int = amount
        """The number of units that the store just bought to the provider"""

class BalanceRecord(Record):
    """This records represents the balance of the store at this point in time"""
    def __init__(self, time: int, balance:int) -> None:
        super().__init__(time)
        self.balance:int = balance
        """The balance of the store at this point in time"""

class PayHoldingRecord(Record):
    """This record represents the amount of money the store is paying for the storage service at a point in time"""
    def __init__(self, time: int, cost:int) -> None:
        super().__init__(time)
        self.cost:int = cost
        """The amount of money the store is paying for the storage service"""
