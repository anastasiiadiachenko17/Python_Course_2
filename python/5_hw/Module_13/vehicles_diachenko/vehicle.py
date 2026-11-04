"""Base dataclass for all vehicles."""

from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Vehicle:
    """A vehicle that can drive and tell the cost of a trip.

    Attributes:
        wheels: Number of wheels, shared by all vehicles of the class.
        fuel_price: Price of one litre of fuel in USD, shared by all
            vehicles.
        FIRST_CAR_YEAR: Earliest valid production year.
        brand: Brand of the vehicle.
        model: Model of the vehicle.
        year: Year the vehicle was made.
        fuel_consumption: Litres of fuel per 100 km.
    """

    wheels: ClassVar[int] = 4
    fuel_price: ClassVar[float] = 50.0
    FIRST_CAR_YEAR: ClassVar[int] = 1886

    brand: str
    model: str
    year: int
    fuel_consumption: float = field(compare=False)
    _mileage: int = field(default=0, init=False, repr=False, compare=False)

    def __post_init__(self):
        """Check the values given to the generated constructor.

        Raises:
            ValueError: If brand or model is empty, year is before
                FIRST_CAR_YEAR, or fuel_consumption is not positive.
        """
        for label, text in (("brand", self.brand), ("model", self.model)):
            if not text:
                raise ValueError(f"{label} must not be empty")

        if self.year < self.FIRST_CAR_YEAR:
            raise ValueError(
                f"year must be {self.FIRST_CAR_YEAR} or later, "
                f"got {self.year}"
            )

        if self.fuel_consumption <= 0:
            raise ValueError(
                "fuel_consumption must be positive, "
                f"got {self.fuel_consumption}"
            )

    @property
    def full_name(self):
        """The brand and the model joined with a space."""
        return f"{self.brand} {self.model}"

    @property
    def mileage(self):
        """Kilometres driven so far, read-only: change it with drive()."""
        return self._mileage

    @classmethod
    def set_fuel_price(cls, price):
        """Set the fuel price for every vehicle of the class.

        Args:
            price: New price of one litre of fuel in USD, positive.

        Raises:
            TypeError: If price is not a number.
            ValueError: If price is zero or negative.
        """
        if not isinstance(price, (int, float)) or isinstance(price, bool):
            raise TypeError(f"price must be a number, got {price!r}")
        if price <= 0:
            raise ValueError(f"price must be positive, got {price}")

        cls.fuel_price = price

    def drive(self, distance):
        """Add a trip to the mileage.

        Args:
            distance: Kilometres driven, zero or more.

        Returns:
            The new mileage.

        Raises:
            ValueError: If distance is negative.
        """
        if distance < 0:
            raise ValueError(f"distance must not be negative, got {distance}")

        self._mileage += distance
        return self._mileage

    def trip_cost(self, distance):
        """Return the fuel cost of a trip.

        Args:
            distance: Kilometres to drive.

        Returns:
            The cost of the trip in USD.
        """
        return distance / 100 * self.fuel_consumption * self.fuel_price

    def describe(self):
        """Return a short description of the vehicle.

        Returns:
            The class name, full name, year and number of wheels.
        """
        return (
            f"{type(self).__name__} {self.full_name} ({self.year}), "
            f"{self.wheels} wheels"
        )

    def __str__(self):
        """Return the description of the vehicle with its mileage.

        Returns:
            The text of describe() followed by the mileage.
        """
        return f"{self.describe()}, {self.mileage} km"
