
class PodType:
    def __init__(self, type_id, capacity: float) -> None:
        self.type_id = type_id
        self.capacity = capacity
        self.description = "None"


class Pod:
    def __init__(self, pod_id, pod_type: PodType) -> None:
        self.id = pod_id
        self.type = pod_type
        self.remainder = pod_type.capacity

    def dose(self, amount):
        self.remainder -= amount


