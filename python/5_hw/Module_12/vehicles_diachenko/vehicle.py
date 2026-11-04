"""Base class for all vehicles."""


class Vehicle:
    """A vehicle that can drive and tell the cost of a trip.

    Attributes:
        wheels: Number of wheels, shared by all vehicles of the class.
        fuel_price: Price of one litre of fuel in USD, shared by all
            vehicles.
        brand: Brand of the vehicle.
        model: Model of the vehicle.
        year: Year the vehicle was made.
        fuel_consumption: Litres of fuel per 100 km.
        mileage: Kilometres driven so far.
    """

    wheels = 4
    fuel_price = 50.0

    def __init__(self, brand, model, year, fuel_consumption):
        """Create a vehicle that has not driven yet.

        Args:
            brand: Brand of the vehicle, must not be empty.
            model: Model of the vehicle, must not be empty.
            year: Year the vehicle was made.
            fuel_consumption: Litres of fuel per 100 km.

        Raises:
            ValueError: If brand or model is empty.
        """
        for label, text in (("brand", brand), ("model", model)):
            if not text:
                raise ValueError(f"{label} must not be empty")

        self.brand = brand
        self.model = model
        self.year = year
        self.fuel_consumption = fuel_consumption
        self.mileage = 0

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

        self.mileage += distance
        return self.mileage

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
            The class name, brand, model, year and number of wheels.
        """
        return (
            f"{type(self).__name__} {self.brand} {self.model} "
            f"({self.year}), {self.wheels} wheels"
        )

    def __str__(self):
        """Return the description of the vehicle with its mileage.

        Returns:
            The text of describe() followed by the mileage.
        """
        return f"{self.describe()}, {self.mileage} km"

    def __repr__(self):
        """Return a text that looks like the constructor call.

        Returns:
            The class name with brand, model, year and fuel consumption.
        """
        return (
            f"{type(self).__name__}({self.brand!r}, {self.model!r}, "
            f"{self.year!r}, {self.fuel_consumption!r})"
        )

    def __eq__(self, other):
        """Tell whether two vehicles have the same brand, model and year.

        The mileage is not compared.

        Args:
            other: Object to compare with.

        Returns:
            True if both are vehicles with the same brand, model and
            year, False if not, or NotImplemented for other objects.
        """
        if not isinstance(other, Vehicle):
            return NotImplemented

        return (self.brand, self.model, self.year) == (
            other.brand,
            other.model,
            other.year,
        )
