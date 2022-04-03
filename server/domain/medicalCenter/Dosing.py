from domain.medicalCenter.Feedback import Feedback


# maybe make Dosing immutable (except for feedback), there's no need to change it as it serves as a history record
# @dataclass(frozen=True) + from dataclasses import dataclass - in python 3.7+
class Dosing:
    def __init__(self, dosing_id, pod_id, time, location) -> None:
        self.id = -1
        self.pod_id = -1
        self.time = -1
        self.location = (-1, -1)
        self.feedback = None




