"""
Parking lot LLD implementation inspired by:
'Low-Level Design Interview Question: Parking System' (Mehar Chand). See source linked in chat.
"""

from enum import Enum
from datetime import datetime, timedelta
import uuid
from collections import defaultdict
from typing import Optional, Dict, List


class VehicleType(Enum):
    MOTORCYCLE = "MOTORCYCLE"
    CAR = "CAR"
    BUS = "BUS"


class Vehicle:
    def __init__(self, license_plate: str, vtype: VehicleType):
        self.license_plate = license_plate
        self.type = vtype

    def __repr__(self):
        return f"{self.type.value}({self.license_plate})"


class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MOTORCYCLE)


class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.CAR)


class Bus(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.BUS)


class SlotType(Enum):
    MOTORCYCLE = "MOTORCYCLE"
    CAR = "CAR"
    BUS = "BUS"


# Rates per hour (as per article)
RATE_PER_HOUR = {
    VehicleType.MOTORCYCLE: 1.0,
    VehicleType.CAR: 2.0,
    VehicleType.BUS: 5.0,
}


class ParkingSlot:
    def __init__(self, level_id: int, slot_num: int, slot_type: SlotType):
        self.level_id = level_id
        self.slot_num = slot_num
        self.slot_type = slot_type
        self.occupied_by: Optional[Vehicle] = None

    def can_accommodate(self, vehicle: Vehicle) -> bool:
        """
        Rules:
         - Motorcycle slot: only motorcycles
         - Car slot: cars and motorcycles
         - Bus slot: buses, cars, motorcycles
        """
        if self.occupied_by is not None:
            return False
        if self.slot_type == SlotType.MOTORCYCLE:
            return vehicle.type == VehicleType.MOTORCYCLE
        if self.slot_type == SlotType.CAR:
            return vehicle.type in (VehicleType.CAR, VehicleType.MOTORCYCLE)
        if self.slot_type == SlotType.BUS:
            return vehicle.type in (VehicleType.BUS, VehicleType.CAR, VehicleType.MOTORCYCLE)
        return False

    def park(self, vehicle: Vehicle):
        if not self.can_accommodate(vehicle):
            raise ValueError("Cannot park here")
        self.occupied_by = vehicle

    def vacate(self):
        self.occupied_by = None

    def is_free(self) -> bool:
        return self.occupied_by is None

    def id(self) -> str:
        return f"L{self.level_id}-S{self.slot_num}"

    def __repr__(self):
        occ = self.occupied_by.license_plate if self.occupied_by else "FREE"
        return f"Slot({self.id()}, {self.slot_type.value}, {occ})"


class ParkingTicket:
    def __init__(self, ticket_id: str, vehicle: Vehicle, slot: ParkingSlot, entry_time: datetime):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.slot = slot
        self.entry_time = entry_time
        self.exit_time: Optional[datetime] = None
        self.fee: Optional[float] = None

    def close(self, exit_time: datetime, fee: float):
        self.exit_time = exit_time
        self.fee = fee

    def duration_hours(self) -> float:
        end = self.exit_time or datetime.now()
        delta = end - self.entry_time
        # compute hours (ceiling to 1 hour blocks, or keep fractional if desired)
        return delta.total_seconds() / 3600.0

    def __repr__(self):
        return (f"Ticket({self.ticket_id}, {self.vehicle.license_plate}, slot={self.slot.id()}, "
                f"entry={self.entry_time}, exit={self.exit_time}, fee={self.fee})")


class BillingService:
    @staticmethod
    def calculate_fee(vehicle_type: VehicleType, duration_hours: float) -> float:
        # Round up to next hour as typical parking lots do:
        hours = int(duration_hours) if duration_hours.is_integer() else int(duration_hours) + 1
        rate = RATE_PER_HOUR.get(vehicle_type, 0.0)
        return hours * rate


class ParkingLevel:
    def __init__(self, level_id: int, num_motorcycle: int, num_car: int, num_bus: int):
        self.level_id = level_id
        self.slots: List[ParkingSlot] = []
        idx = 1
        for _ in range(num_motorcycle):
            self.slots.append(ParkingSlot(level_id, idx, SlotType.MOTORCYCLE)); idx += 1
        for _ in range(num_car):
            self.slots.append(ParkingSlot(level_id, idx, SlotType.CAR)); idx += 1
        for _ in range(num_bus):
            self.slots.append(ParkingSlot(level_id, idx, SlotType.BUS)); idx += 1

        # For quick lookup of free slots by slot type, keep lists (could be heaps for nearest)
        self.free_by_type: Dict[SlotType, List[ParkingSlot]] = defaultdict(list)
        self._rebuild_free_index()

    def _rebuild_free_index(self):
        self.free_by_type = defaultdict(list)
        for s in self.slots:
            if s.is_free():
                self.free_by_type[s.slot_type].append(s)

    def find_slot_for_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSlot]:
        # Prefer smallest slot that fits. That minimizes waste.
        order = []
        if vehicle.type == VehicleType.MOTORCYCLE:
            order = [SlotType.MOTORCYCLE, SlotType.CAR, SlotType.BUS]
        elif vehicle.type == VehicleType.CAR:
            order = [SlotType.CAR, SlotType.BUS]
        elif vehicle.type == VehicleType.BUS:
            order = [SlotType.BUS]
        for st in order:
            for slot in self.free_by_type.get(st, []):
                if slot.can_accommodate(vehicle):
                    return slot
        return None

    def park_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSlot]:
        slot = self.find_slot_for_vehicle(vehicle)
        if not slot:
            return None
        slot.park(vehicle)
        self._rebuild_free_index()
        return slot

    def vacate_slot(self, slot_id: str) -> Optional[ParkingSlot]:
        for s in self.slots:
            if s.id() == slot_id:
                s.vacate()
                self._rebuild_free_index()
                return s
        return None

    def status(self) -> Dict[str, tuple]:
        # returns free/total counts per slot type
        counts = defaultdict(lambda: [0, 0])  # [free, total]
        for s in self.slots:
            t = s.slot_type.value
            counts[t][1] += 1
            if s.is_free():
                counts[t][0] += 1
        return {k: tuple(v) for k, v in counts.items()}


class ParkingLot:
    """
    Singleton ParkingLot for simplicity in this implementation.
    """
    _instance = None

    def __init__(self):
        if ParkingLot._instance is not None:
            raise Exception("ParkingLot is singleton, use get_instance()")
        self.levels: Dict[int, ParkingLevel] = {}
        self.tickets_by_plate: Dict[str, ParkingTicket] = {}
        self.active_tickets: Dict[str, ParkingTicket] = {}
        self.billing_service = BillingService()
        ParkingLot._instance = self

    @staticmethod
    def get_instance():
        if ParkingLot._instance is None:
            ParkingLot()
        return ParkingLot._instance

    def add_level(self, level_id: int, num_motorcycle: int, num_car: int, num_bus: int):
        if level_id in self.levels:
            raise ValueError(f"Level {level_id} already exists")
        self.levels[level_id] = ParkingLevel(level_id, num_motorcycle, num_car, num_bus)
        return f"Level {level_id} added with {num_motorcycle} motorcycle slots, {num_car} car slots, {num_bus} bus slots."

    def park_vehicle(self, vehicle: Vehicle) -> str:
        if vehicle.license_plate in self.active_tickets:
            return f"Vehicle {vehicle.license_plate} already parked."

        # Try levels in increasing level id order (could be optimized for nearest)
        for lid in sorted(self.levels.keys()):
            level = self.levels[lid]
            slot = level.park_vehicle(vehicle)
            if slot:
                ticket_id = str(uuid.uuid4())[:8]
                ticket = ParkingTicket(ticket_id, vehicle, slot, datetime.now())
                self.tickets_by_plate[vehicle.license_plate] = ticket
                self.active_tickets[vehicle.license_plate] = ticket
                return f"{vehicle.type.value.capitalize()} with license plate {vehicle.license_plate} parked at level {lid}, slot {slot.slot_num}. Ticket: {ticket_id}"
        return f"No available slots for {vehicle.type.value}."

    def exit_vehicle(self, license_plate: str) -> str:
        ticket = self.active_tickets.get(license_plate)
        if not ticket:
            return f"Vehicle with license plate {license_plate} not found in parking."
        exit_time = datetime.now()
        duration = (exit_time - ticket.entry_time).total_seconds() / 3600.0
        fee = self.billing_service.calculate_fee(ticket.vehicle.type, duration)
        ticket.close(exit_time, fee)
        # vacate slot
        level = self.levels[ticket.slot.level_id]
        level.vacate_slot(ticket.slot.id())
        # remove active
        del self.active_tickets[license_plate]
        return f"{ticket.vehicle.type.value.capitalize()} with license plate {license_plate} exited. Fee: ${fee:.2f}. Duration: {duration:.2f} hours."

    def view_status(self) -> str:
        lines = []
        for lid in sorted(self.levels.keys()):
            lvl = self.levels[lid]
            stat = lvl.status()
            # Format: Level 1: 5/10 motorcycle slots, 10/20 car slots, 2/5 bus slots available.
            parts = []
            # Ensure order motorcycle, car, bus
            for st in ("MOTORCYCLE", "CAR", "BUS"):
                free, total = stat.get(st, (0, 0))
                parts.append(f"{free}/{total} {st.lower()} slots")
            lines.append(f"Level {lid}: " + ", ".join(parts) + " available.")
        return "\n".join(lines) if lines else "No levels configured."

    # Admin helpers for adding/removing slots (basic)
    def add_slots(self, level_id: int, slot_type: SlotType, number: int):
        level = self.levels.get(level_id)
        if not level:
            raise ValueError("Level not found")
        # append new slots
        current_max = max([s.slot_num for s in level.slots]) if level.slots else 0
        for i in range(1, number + 1):
            level.slots.append(ParkingSlot(level_id, current_max + i, slot_type))
        level._rebuild_free_index()
        return f"Added {number} {slot_type.value} slots to level {level_id}."

    def remove_slots(self, level_id: int, slot_type: SlotType, number: int):
        level = self.levels.get(level_id)
        if not level:
            raise ValueError("Level not found")
        free_of_type = [s for s in level.slots if s.slot_type == slot_type and s.is_free()]
        if len(free_of_type) < number:
            raise ValueError("Not enough free slots to remove")
        # Remove from slots list (remove by slot_num)
        remove_set = set(s.id() for s in free_of_type[:number])
        level.slots = [s for s in level.slots if s.id() not in remove_set]
        level._rebuild_free_index()
        return f"Removed {number} {slot_type.value} slots from level {level_id}."


# -----------------
# Simple CLI-ish usage
# -----------------
def example_run():
    pl = ParkingLot.get_instance()
    print(pl.add_level(1, 2, 3, 1))  # small level
    print(pl.add_level(2, 1, 2, 0))

    print(pl.park_vehicle(Car("KA-01-HH-1234")))
    print(pl.park_vehicle(Motorcycle("KA-01-HH-9999")))
    print(pl.park_vehicle(Bus("KA-02-BB-0001")))

    print("\nStatus:\n", pl.view_status())

    # fake wait: to demonstrate fee, you could adjust entry time in ticket (here we just exit immediately)
    print(pl.exit_vehicle("KA-01-HH-1234"))
    print("\nStatus after exit:\n", pl.view_status())


if __name__ == "__main__":
    example_run()
