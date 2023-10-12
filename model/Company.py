class Company:
    def __init__(self, id: str, name: str, vehicles: list, drivers: list, managers: list):
        self.id: str = id
        self.name: str = name
        self.vehicles: list = vehicles
        self.drivers: list = drivers
        self.managers: list = managers
