from db import add_vehicle, exit_vehicle

class ParkedVehicle:
    def __init__(self, plate_number, vehicle_type):
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type

    def park(self):
        """Saves vehicle entry in the database."""
        return add_vehicle(self.plate_number, self.vehicle_type)

    def leave(self):
        """Processes vehicle exit and calculates fare."""
        return exit_vehicle(self.plate_number)
