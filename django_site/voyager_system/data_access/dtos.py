'''
data classes passed to the database update funtions.
'''
class AccountDto:
    # def __init__(self, id, email, f_name, l_name, phone, dob, registration_date) -> None:
    def __init__(self) -> None:
        self.id = None #id
        self.email = None #email
        self.f_name = None #f_name
        self.l_name = None #l_name
        self.phone = None #phone
        self.dob = None #dob
        self.registration_date = None #registration_date


class ConsumerDto:
    def __init__(self) -> None:
        # dispenser-related relations
        # self.dispensers = []                    # 1-to-n (?)
        # self.pods = []                          # 1-to-n
        # self.dosing_history = []                # 1-to-n
        self.id = None
        # personal info
        self.residence = None
        self.height = None
        self.weight = None
        self.gender = None
        self.units = None
        self.goal = None

class DispenserDto:
    def __init__(self) -> None:
        self.serial_num = None
        self.version = None
        self.consumer = None
        self.registration_date = None


class PodTypeDto:
    def __init__(self) -> None:
        self.name = None
        self.company = None
        self.substance = None
        self.capacity = None
        self.description = None
        self.url = None

class PodDto:
    def __init__(self) -> None:
        self.serial_num = None
        self.pod_type = PodTypeDto()
        self.remainder = None

class DosingDto:
    def __init__(self) -> None:
        self.pod = PodDto()
        self.time = None
        self.latitude = None
        self.longitude = None

class RegimenDto:
    def __init__(self) -> None:
        self.schedule = dict()#podType -> (day, time) -> ammount

class FeedbackDto:
    def __init__(self) -> None:
        self.dosing = DosingDto()
        self.rating = None
        self.comment = None

class FeedbackReminderDto:
    def __init__(self) -> None:
        self.dosing = DosingDto()
        self.time = None