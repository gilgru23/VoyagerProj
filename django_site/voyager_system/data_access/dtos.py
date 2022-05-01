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

        # personal info
        self.residence = None
        self.height = None
        self.weight = None
        self.gender = None
        self.goal = None

class DispenserDto:
    def __init__(self) -> None:
        self.serial_num = None
        self.version = None
        self.consumer = None
        self.registration_date = None


