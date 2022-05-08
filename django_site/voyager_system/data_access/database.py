from typing import List
from accounts.models import Account
from consumer_app.models import Consumer, Dispenser, Pod, PodType, Business, Company
from voyager_system.data_access.dtos import FeedbackDto, FeedbackReminderDto

from voyager_system.data_access.dtos import AccountDto, ConsumerDto, DispenserDto, PodTypeDto, PodDto, DosingDto, \
    RegimenDto


# region Account
def has_account_with_email(email):
    return Account.objects.filter(email=email).exists()


def has_account_with_id(id):
    return Account.objects.filter(id=id).exists()


def add_account(email, f_name, l_name, phone, dob):
    account = Account.objects.create(email=email, f_name=f_name, l_name=l_name, phone=phone, dob=dob)
    return account


def add_account_from_dto(acct_dto: AccountDto):
    # email, phone, f_name, l_name, dob
    account = Account.objects.create(
        email=acct_dto.email, f_name=acct_dto.f_name, l_name=acct_dto.l_name, phone=acct_dto.phone, dob=acct_dto.dob
    )
    return account


def get_account_by_email(email: str) -> AccountDto:
    account = Account.objects.get(email=email)
    dto = AccountDto()
    dto.id = account.id
    dto.email = account.email
    dto.f_name = account.f_name
    dto.l_name = account.l_name
    # dto.phone = account.phone
    dto.dob = account.dob
    dto.registration_date = account.registration_date
    return dto


def get_account_by_id(id: int) -> AccountDto:
    account = Account.objects.get(id=id)
    dto = AccountDto()
    dto.id = account.id
    dto.email = account.email
    dto.f_name = account.f_name
    dto.l_name = account.l_name
    # dto.phone = account.phone
    dto.dob = account.dob
    dto.registration_date = account.registration_date
    return dto


def update_account(acct_dto: AccountDto):
    acct: Account = Account.objects.get(id=acct_dto.id)
    acct.email = acct_dto.email
    acct.phone = acct_dto.phone
    acct.f_name = acct_dto.f_name
    acct.l_name = acct_dto.l_name
    acct.phone = acct_dto.phone
    acct.save()


# endregion Account


# region Consumer
def add_consumer(id: int, residence: str, height: int, weight: int, units: int, gender: int, goal: any):
    return Consumer.objects.create(
        account=Account.objects.get(id=id),
        residence=residence, height=height, weight=weight,
        units=units, gender=gender  # , goal=goal
    )


def get_consumer(account_id: int) -> ConsumerDto:
    consumer = Consumer.objects.get(account=account_id)
    dto = ConsumerDto()
    dto.residence = consumer.residence
    dto.height = consumer.height
    dto.weight = consumer.weight
    dto.units = consumer.units
    dto.gender = consumer.gender
    return dto


def has_consumer(id):
    return Consumer.objects.filter(account_id=id).exists()


def update_consumer(consumer_dto: ConsumerDto):
    cons: Consumer = Consumer.objects.get(account_id=consumer_dto.id)
    cons.residence = consumer_dto.residence
    cons.height = consumer_dto.height
    cons.weight = consumer_dto.weight
    cons.units = consumer_dto.units
    cons.gender = consumer_dto.gender
    cons.goal = consumer_dto.goal
    cons.save()


# dispenser
def add_dispenser(dispenser_dto: DispenserDto):
    return Dispenser.objects.create(serial_num=dispenser_dto.serial_num,
                                    version=dispenser_dto.version)


def get_dispenser(serial_num: str) -> Dispenser:
    return Dispenser.objects.get(serial_num=serial_num)


# todo: depreciate, use update_dispenser instead
def set_dispenser_consumer(serial_num: str, consumer_id: int):
    dispenser = Dispenser.objects.get(serial_num=serial_num)
    dispenser.consumer_id = consumer_id
    dispenser.save()


def update_dispenser(dispenser_dto: DispenserDto, consumer_id: int):
    disp: Dispenser = Dispenser.objects.get(serial_num=dispenser_dto.serial_num)

    disp.version = dispenser_dto.version
    disp.consumer = Consumer.objects.get(account_id=consumer_id)
    disp.registration_date = dispenser_dto.registration_date
    disp.save()


# endregion Consumer


# region Pod Type
def add_pod_type(company_name: str, pod_type_dto: PodTypeDto):
    pod_type = PodType.objects.create(name=pod_type_dto.name,
                                      company=Company.objects.get(business=Business.objects.get(name=company_name)),
                                      substance=pod_type_dto.substance,
                                      description=pod_type_dto.description,
                                      url=pod_type_dto.url)
    return pod_type


def get_pod_type(pod_type_name: str) -> PodTypeDto:
    pod_type = PodType.objects.get(name=pod_type_name)
    dto = PodTypeDto()
    dto.name = pod_type.name
    dto.company = pod_type.company
    dto.substance = pod_type.substance
    # dto.capacity = pod_type.capacity
    dto.description = pod_type.description
    dto.url = pod_type.url
    return dto


def update_pod_type(pod_type_dto: PodTypeDto):
    pass


def get_pod_types_by_company(company_name: str) -> List[PodTypeDto]:
    pass


# endregion Pod Type


# region Pod
def add_pod(consumer_id, pod_type_name: str, pod_dto: PodDto):
    pod = Pod.objects.create(serial_num=pod_dto.serial_num,
                             pod_type=PodType.objects.get(name=pod_type_name),
                             remainder=pod_dto.serial_num,
                             consumer=Consumer.objects.get(account_id=consumer_id))
    return pod


def get_pods_for_consumer_by_id(consumer_id: int) -> List[PodDto]:
    # pods = Pod.objects.filter(consumer=Consumer.objects.get(account_id=consumer_id))
    # pods_dtos = [pod_to_dto(pod) for pod in pods]
    # return pods_dtos
    pass


def get_pod_by_id(pod_id: int) -> PodDto:
    pass

def get_pod_by_serial_number(serial_number: str) -> PodDto:
    pod = Pod.objects.get(serial_num=serial_number)
    dto = pod_to_dto(pod)
    return dto


def get_pods_by_email(email: str) -> List[PodDto]:
    pass


def update_pod(pod_dto: PodDto, pod_type_name: str, consumer_id: int):
    pod = Pod.objects.get(serial_num=pod_dto.serial_num)
    pod.consumer = Consumer.objects.get(account_id=consumer_id)
    pod.pod_type = PodType.objects.get(name=pod_type_name)
    pod.remainder = pod_dto.remainder
    pod.save()


def pod_to_dto(pod):
    dto = PodDto()
    dto.pod_type = get_pod_type(pod.pod_type.name)
    dto.serial_num = pod.serial_num
    dto.remainder = pod.remainder
    return dto


# endregion Pod


# region Dosing
def add_dosing(dosing_dto: DosingDto):
    pass


def get_dosings_for_consumer_by_id(consumer_id: int) -> List[DosingDto]:
    pass


def get_dosings_for_consumer_by_email(consumer_email: str) -> List[DosingDto]:
    pass


def get_dosings_for_pod(pod_dto: PodDto) -> List[DosingDto]:
    pass


# endregion Dosing


# region Regimen
# type,day,time,amount
def add_to_regimen_with_id(consumer_id: int, pod_type_name: str, day: int, time: int, amount: float):
    pass


def add_to_regimen_with_email(consumer_email: str, pod_type_name: str, day: int, time: int, amount: float):
    pass


def get_regimen_by_consumer_id(consumer_id: int) -> RegimenDto:
    pass


def get_regimen_by_consumer_email(consumer_email: str) -> RegimenDto:
    pass


# endregion Regimen


# region Feedback
def add_feedback(feedback_dto: FeedbackDto):
    pass


def get_feedbacks_for_consumer(consumer_id: int) -> List[FeedbackDto]:
    pass


# endregion Feedback


# region Feedback Reminder
def add_feedback_reminder(feedback_reminder_dto: FeedbackReminderDto):
    pass


def get_all_feedback_reminders_in_time_window(from_time, until_time) -> List[FeedbackReminderDto]:
    pass


# endregion Feedback Reminder

def add_company(business_name: str):
    Business.objects.create(name=business_name, docs_path="/")
    company = Company.objects.create(business=Business.objects.get(name=business_name))
    return company
