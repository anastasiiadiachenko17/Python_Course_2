"""Car, a vehicle with seats."""

from vehicle import Vehicle


class Car(Vehicle):
    """A vehicle that carries passengers.

    Attributes:
        seats: Number of seats.
    """

    def __init__(self, brand, model, year, fuel_consumption, seats=5):
        """Create a car that has not driven yet.

        Args:
            brand: Brand of the car, must not be empty.
            model: Model of the car, must not be empty.
            year: Year the car was made.
            fuel_consumption: Litres of fuel per 100 km.
            seats: Number of seats.

        Raises:
            ValueError: If brand or model is empty.
        """
        super().__init__(brand, model, year, fuel_consumption)
        self.seats = seats

    def describe(self):
        """Return a short description of the car.

        Returns:
            The description of the vehicle followed by the seats.
        """
        return f"{super().describe()}, {self.seats} seats"
