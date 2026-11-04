"""Show how the Vehicle, Car and Truck classes work together."""

from car import Car
from truck import Truck
from vehicle import Vehicle

TRIP_KM = 200
DRIVE_KM = 120
CARGO_TONS = 10
EXTRA_CARGO_TONS = 15
NEW_FUEL_PRICE = 60


def print_trip_costs(car, truck):
    """Print the cost of a trip for the car and the truck.

    Args:
        car: Car to price the trip for.
        truck: Truck to price the trip for.
    """
    print(f"Car:   {car.trip_cost(TRIP_KM):.2f} USD")
    print(f"Truck: {truck.trip_cost(TRIP_KM):.2f} USD")


def main():
    """Create the vehicles and print what each of them can do."""
    vehicle = Vehicle("Generic", "Cart", 1999, 4.0)
    car = Car("Toyota", "Corolla", 2015, 6.5)
    truck = Truck("Volvo", "FH16", 2020, 28.0, 20)

    vehicles = [vehicle, car, truck]

    print("--- describe() for every vehicle ---")
    for each_vehicle in vehicles:
        print(each_vehicle.describe())

    print("\n--- repr() and str() ---")
    print(repr(car))
    print(str(truck))

    print("\n--- drive() ---")
    print(f"Mileage after the trip: {car.drive(DRIVE_KM)}")
    print(car)

    print(f"\n--- trip_cost({TRIP_KM}) ---")
    print_trip_costs(car, truck)

    print("\n--- loading the truck ---")
    print(f"Load: {truck.load_cargo(CARGO_TONS)} t")
    print(f"Truck: {truck.trip_cost(TRIP_KM):.2f} USD")
    try:
        truck.load_cargo(EXTRA_CARGO_TONS)
    except ValueError as error:
        print(error)

    print(f"\n--- Vehicle.set_fuel_price({NEW_FUEL_PRICE}) ---")
    Vehicle.set_fuel_price(NEW_FUEL_PRICE)
    print_trip_costs(car, truck)

    print("\n--- __eq__ ---")
    same_car = Car("Toyota", "Corolla", 2015, 6.5)
    print(f"car == same_car: {car == same_car}")
    print(f"car == truck: {car == truck}")

    print("\n--- class defaults ---")
    print(f"Truck.wheels = {Truck.wheels}, Vehicle.wheels = {Vehicle.wheels}")


if __name__ == "__main__":
    main()
