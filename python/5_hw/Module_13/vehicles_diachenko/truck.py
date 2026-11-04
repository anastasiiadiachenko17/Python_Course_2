"""Truck, a dataclass vehicle that carries cargo."""

from dataclasses import dataclass, field
from typing import ClassVar

from vehicle import Vehicle


@dataclass
class Truck(Vehicle):
    """A vehicle whose trips cost more the heavier its cargo is.

    Attributes:
        wheels: Number of wheels, six for every truck.
        LOAD_PENALTY: Share by which each ton of cargo raises the fuel
            consumption.
        capacity_tons: Largest load the truck can carry, in tons.
    """

    wheels: ClassVar[int] = 6
    LOAD_PENALTY: ClassVar[float] = 0.1

    capacity_tons: int
    _load: int = field(default=0, init=False, repr=False, compare=False)

    @property
    def load(self):
        """Tons of cargo on the truck now."""
        return self._load

    @load.setter
    def load(self, tons):
        """Put a new load on the truck.

        Args:
            tons: New load in tons.

        Raises:
            ValueError: If tons is negative or exceeds the capacity.
                The load stays unchanged.
        """
        if tons < 0:
            raise ValueError(f"load must not be negative, got {tons}")
        if tons > self.capacity_tons:
            raise ValueError(
                f"Overload: {tons} t exceeds capacity of "
                f"{self.capacity_tons} t"
            )

        self._load = tons

    @property
    def free_capacity(self):
        """Tons of cargo that still fit on the truck."""
        return self.capacity_tons - self.load

    def trip_cost(self, distance):
        """Return the fuel cost of a trip with the current cargo.

        Args:
            distance: Kilometres to drive.

        Returns:
            The cost of the trip in USD, raised by LOAD_PENALTY for
            each ton of cargo.
        """
        return super().trip_cost(distance) * (
            1 + self.LOAD_PENALTY * self.load
        )

    def describe(self):
        """Return a short description of the truck.

        Returns:
            The description of the vehicle followed by the load and
            the capacity.
        """
        return f"{super().describe()}, {self.load}/{self.capacity_tons} t"
