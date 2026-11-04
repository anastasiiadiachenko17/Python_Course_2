"""Car, a dataclass vehicle with seats."""

from dataclasses import dataclass
from typing import ClassVar

from vehicle import Vehicle


@dataclass
class Car(Vehicle):
    """A vehicle that carries passengers.

    Attributes:
        FAMILY_SEATS: Smallest number of seats of a family car.
        seats: Number of seats.
    """

    FAMILY_SEATS: ClassVar[int] = 6

    seats: int = 5

    @property
    def is_family_car(self):
        """True if the car has at least FAMILY_SEATS seats."""
        return self.seats >= self.FAMILY_SEATS

    def describe(self):
        """Return a short description of the car.

        Returns:
            The description of the vehicle followed by the seats.
        """
        return f"{super().describe()}, {self.seats} seats"
