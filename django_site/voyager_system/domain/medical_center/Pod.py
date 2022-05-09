class PodType:
    def __init__(self, name: str = None, capacity: float = 20,company: str = None,
                 substance: str = None, description: str = None) -> None:
        self.name = name
        self.capacity = capacity
        self.company = company
        self.substance = substance
        self.description = description
        self.url = "None"


class Pod:
    def __init__(self, serial_number: str = None, pod_type: PodType = None) -> None:
        self.serial_number = serial_number
        self.type = pod_type
        if pod_type:
            self.remainder = pod_type.capacity

    def dose(self, amount):
        self.remainder -= amount
