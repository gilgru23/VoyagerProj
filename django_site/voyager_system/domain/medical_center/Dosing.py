

# maybe make Dosing immutable (except for feedback), there's no need to change it as it serves as a history record
# @dataclass(frozen=True) + from dataclasses import dataclass - in python 3.7+
class Dosing:
    def __init__(self, dosing_id, pod_serial_number, amount: float, time, latitude, longitude) -> None:
        self.id = dosing_id
        self.pod_serial_number = pod_serial_number
        # self.pod_type_name = pod_type_name
        self.amount = amount
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.feedback = None


class Feedback:
    def __init__(self, id, dosing_id, rating, comment, time) -> None:
        self.id = id
        self.dosing_id = dosing_id
        self.rating = rating
        self.comment = comment
        self.time = time


class DosingReminder:
    pass


class FeedbackReminder:
    pass


