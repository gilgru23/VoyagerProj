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

    def __init__(self, serial_number: str = None, remainder: float = None, type_name: str = None, obj_version = None) -> None:
        self.serial_number = serial_number
        self.type_name = type_name
        self.remainder = remainder
        self.obj_version = obj_version

    @staticmethod
    def from_type(serial_number: str, pod_type: PodType):
        pod: Pod = Pod()
        pod.serial_number = serial_number
        pod.type_name = pod_type.name
        pod.remainder = pod_type.capacity
        return pod

    def dose(self, amount):
        self.remainder -= amount
