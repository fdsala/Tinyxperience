import datetime
from dataclasses import dataclass, field
from typing import List

@dataclass
class Extra:
    name: str
    price_per_day: float

@dataclass
class Vehicle:
    name: str
    daily_rate: float

@dataclass
class RentalQuote:
    vehicle: Vehicle
    start_date: datetime.date
    end_date: datetime.date
    extras: List[Extra] = field(default_factory=list)

    @property
    def days(self) -> int:
        return (self.end_date - self.start_date).days + 1

    def calculate_total(self) -> float:
        base = self.days * self.vehicle.daily_rate
        extras_cost = sum(extra.price_per_day * self.days for extra in self.extras)
        return base + extras_cost

VEHICLES = {
    "compact": Vehicle("Compact", 50),
    "suv": Vehicle("SUV", 80),
    "van": Vehicle("Van", 100),
}

EXTRAS = {
    "gps": Extra("GPS", 5),
    "child_seat": Extra("Child Seat", 5),
}

def parse_date(date_str: str) -> datetime.date:
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


def main():
    print("Available vehicles:")
    for key, vehicle in VEHICLES.items():
        print(f"  {key}: {vehicle.name} (${vehicle.daily_rate}/day)")
    vehicle_key = input("Choose vehicle type: ").strip().lower()
    vehicle = VEHICLES.get(vehicle_key)
    if not vehicle:
        raise SystemExit("Invalid vehicle type")

    start_str = input("Start date (YYYY-MM-DD): ")
    end_str = input("End date (YYYY-MM-DD): ")
    start_date = parse_date(start_str)
    end_date = parse_date(end_str)
    if end_date < start_date:
        raise SystemExit("End date must be after start date")

    chosen_extras: List[Extra] = []
    print("Optional extras (comma separated keys, blank for none):")
    for key, extra in EXTRAS.items():
        print(f"  {key}: {extra.name} (${extra.price_per_day}/day)")
    extras_input = input("Extras: ").strip().lower()
    if extras_input:
        for key in extras_input.split(','):
            key = key.strip()
            extra = EXTRAS.get(key)
            if extra:
                chosen_extras.append(extra)

    quote = RentalQuote(vehicle, start_date, end_date, chosen_extras)
    total = quote.calculate_total()
    print(f"\nRental summary:")
    print(f"Vehicle: {quote.vehicle.name}")
    print(f"Days: {quote.days}")
    if quote.extras:
        for extra in quote.extras:
            print(f"Extra: {extra.name} (${extra.price_per_day}/day)")
    print(f"Total cost: ${total:.2f}")

if __name__ == "__main__":
    main()
