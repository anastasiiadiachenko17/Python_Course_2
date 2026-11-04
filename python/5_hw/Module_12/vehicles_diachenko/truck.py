"""Truck, a vehicle that carries cargo."""

from vehicle import Vehicle


class Truck(Vehicle):
    """A vehicle whose trips cost more the heavier its cargo is.

    Attributes:
        wheels: Number of wheels, six for every truck.
        LOAD_PENALTY: Share by which each ton of cargo raises the fuel
            consumption.
        capacity_tons: Largest load the truck can carry, in tons.
        load: Tons of cargo on the truck now.
    """

    wheels = 6
    LOAD_PENALTY = 0.1

    def __init__(self, brand, model, year, fuel_consumption, capacity_tons):
        """Create an empty truck that has not driven yet.

        Args:
            brand: Brand of the truck, must not be empty.
            model: Model of the truck, must not be empty.
            year: Year the truck was made.
            fuel_consumption: Litres of fuel per 100 km.
            capacity_tons: Largest load the truck can carry, in tons.

        Raises:
            ValueError: If brand or model is empty.
        """
        super().__init__(brand, model, year, fuel_consumption)
        self.capacity_tons = capacity_tons
        self.load = 0

    def load_cargo(self, tons):
        """Add cargo to the truck.

        Args:
            tons: Tons of cargo to add.

        Returns:
            The new load in tons.

        Raises:
            ValueError: If the new load would exceed the capacity. The
                load stays unchanged.
        """
        new_load = self.load + tons
        if new_load > self.capacity_tons:
            raise ValueError(
                f"Overload: {new_load} t exceeds capacity of "
                f"{self.capacity_tons} t"
            )

        self.load = new_load
        return self.load

    def unload(self):
        """Remove all cargo from the truck."""
        self.load = 0

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
