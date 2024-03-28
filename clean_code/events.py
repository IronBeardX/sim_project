from typing import Self


class Event:
    def __init__(self, time: int = 0, priority: int = 0) -> None:
        self.time: int = time
        self.priority = priority
        """This is the time in which the event should be processed"""

    def __lt__(self, other: Self):
        if self.time == other.time:
            return self.priority < other.priority
        return self.time < other.time


class SimulationEndEvent(Event):
    """This event tells the simulation that must finish everything"""

    def __init__(self, time: int) -> None:
        super().__init__(time, 0)


class SupplyArrivalEvent(Event):
    """This event represents the number of units that the store receives by it's supplier"""

    def __init__(self, time: int, amount: int) -> None:
        super().__init__(time, 1)
        self.amount: int = amount
        """This variable represents the number of Units received by the store by it's supplier"""


class SellEvent(Event):
    """This event represents a client that wants to buy some units of the product"""

    def __init__(self, time: int, amount: int) -> None:
        super().__init__(time, 2)
        self.amount: int = amount
        """This variable represents the number of units the client wants to buy"""


class PayHoldingEvent(Event):
    """This event represents the moment in which the store should pay for the storage service"""

    def __init__(self, time: int) -> None:
        super().__init__(time, 3)
