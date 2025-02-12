from datetime import datetime

class ParkedVehicle:
    def __init__(self, vehicle_type, plate_number, entry_time, exit_time=None):
        self.vehicle_type = vehicle_type
        self.plate_number = plate_number
        self.entry_time = datetime.strptime(entry_time, "%Y-%m-%d %H:%M:%S")
        self.exit_time = datetime.strptime(exit_time, "%Y-%m-%d %H:%M:%S") if exit_time else None

    def calculate_fare(self):
        if not self.exit_time:
            return 0.0
        duration = (self.exit_time - self.entry_time).total_seconds() / 3600
        rate = 50 if self.vehicle_type.lower() == "car" else 20
        return round(duration * rate, 2)
