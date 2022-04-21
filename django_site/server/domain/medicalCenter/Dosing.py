# from server.domain.medicalCenter.Feedback import Feedback


# maybe make Dosing immutable (except for feedback), there's no need to change it as it serves as a history record
# @dataclass(frozen=True) + from dataclasses import dataclass - in python 3.7+
class Dosing:
    def __init__(self, dosing_id, pod_id,amount:float, time, location) -> None:
        self.id = dosing_id
        self.pod_id = pod_id
        self.amount = amount
        self.time = time
        self.location = location
        self.feedback = None


class Feedback:
    def __init__(self, id, rating, description, time) -> None:
        self.id = id
        self.rating = rating
        self.description = description
        self.time = time




