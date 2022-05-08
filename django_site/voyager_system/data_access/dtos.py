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

    def build(self, id, email, f_name, l_name, phone, dob, registration_date):
        self.id = id
        self.email = email
        self.f_name = f_name
        self.l_name = l_name
        self.phone = phone
        self.dob = dob
        self.registration_date = registration_date
        return self



class ConsumerDto:
    def __init__(self) -> None:
        self.id = None
        self.residence = None
        self.height = None
        self.weight = None
        self.gender = None
        self.units = None
        self.goal = None
        
    def build(self, id, residence, height, weight, gender, units, goal):
        self.id = id
        self.residence = residence
        self.height = height
        self.weight = weight
        self.gender = gender
        self.units = units
        self.goal = goal
        return self

class DispenserDto:
    def __init__(self) -> None:
        self.serial_num = None
        self.version = None
        self.consumer = None
        self.registration_date = None
    
    def build(self, serial_num, version, consumer, registration_date):
        self.serial_num = serial_num
        self.version = version
        self.consumer = consumer
        self.registration_date = registration_date
        return self


class PodTypeDto:
    def __init__(self) -> None:
        self.name = None
        self.company = None
        self.substance = None
        self.capacity = None
        self.description = None
        self.url = None

    def build(self, name, company, substance, capacity, description, url):
        self.name = name
        self.company = company
        self.substance = substance
        self.capacity = capacity
        self.description = description
        self.url = url
        return self

class PodDto:
    def __init__(self) -> None:
        self.serial_num = None
        self.pod_type = PodTypeDto()
        self.remainder = None

    def build(self, serial_num, pod_type, remainder):
        self.serial_num = serial_num
        self.pod_type = pod_type
        self.remainder = remainder
        return self

class DosingDto:
    def __init__(self) -> None:
        self.id = None
        self.pod = None #serial number
        self.time = None
        self.latitude = None
        self.longitude = None

    def build(self, id, pod, time, latitude, longitude):
        self.id = id,
        self.pod = pod
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        return self

class RegimenDto:
    def __init__(self) -> None:
        self.schedule = dict()#podType -> (day, time) -> ammount

    def build(self, schedule):
        self.schedule = schedule
        return self

class FeedbackDto:
    def __init__(self) -> None:
        self.dosing = DosingDto()
        self.rating = None
        self.comment = None

    def build(self, dosing, rating, comment):
        self.dosing = dosing
        self.rating = rating
        self.comment = comment
        return self

class FeedbackReminderDto:
    def __init__(self) -> None:
        self.dosing = DosingDto()
        self.time = None

    def build(self, dosing, time):
        self.dosing = dosing
        self.time = time
        return self