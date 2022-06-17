from time import time, sleep
from turtle import pos
from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from account_api.models import Account
from consumer_api.models import Consumer, Dispenser, Pod, PodType, Business, Company, Dosing, Feedback, \
    FeedbackReminder, Regimen, Caregiver
from voyager_system.common.ErrorTypes import ConcurrentUpdateError
from voyager_system.data_access.dtos import AccountDto, ConsumerDto, DispenserDto, PodTypeDto, PodDto, DosingDto, \
    RegimenDto, FeedbackDto, FeedbackReminderDto, CaregiverDto


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
    dto.obj_version = account.obj_version
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
    if acct.obj_version != acct_dto.obj_version:
        raise ConcurrentUpdateError()
    acct.email = acct_dto.email
    acct.phone = acct_dto.phone
    acct.f_name = acct_dto.f_name
    acct.l_name = acct_dto.l_name
    acct.phone = acct_dto.phone
    acct.obj_version = acct_dto.obj_version + 1
    acct.save()


# endregion Account

# region Consumer
def _id_to_consumer(consumer_id: int) -> Consumer:
    return Consumer.objects.get(account=consumer_id)


def add_consumer(id: int, residence: str, height: int, weight: int, units: int, gender: int, goal: any):
    return Consumer.objects.create(
        account=Account.objects.get(id=id),
        residence=residence, height=height, weight=weight,
        units=units, gender=gender  # , goal=goal
    )


def get_consumer(account_id: int) -> ConsumerDto:
    consumer = Consumer.objects.get(account=account_id)
    dto: ConsumerDto = ConsumerDto()
    dto.id = account_id
    dto.residence = consumer.residence
    dto.height = consumer.height
    dto.weight = consumer.weight
    dto.units = consumer.units
    dto.gender = consumer.gender
    dto.obj_version = consumer.obj_version
    return dto


def has_consumer(id):
    return Consumer.objects.filter(account_id=id).exists()


def update_consumer(consumer_dto: ConsumerDto):
    cons: Consumer = Consumer.objects.get(account_id=consumer_dto.id)
    if cons.obj_version != consumer_dto.obj_version:
        raise ConcurrentUpdateError()
    cons.residence = consumer_dto.residence
    cons.height = consumer_dto.height
    cons.weight = consumer_dto.weight
    cons.units = consumer_dto.units
    cons.gender = consumer_dto.gender
    cons.goal = consumer_dto.goal
    cons.obj_version = consumer_dto.obj_version + 1
    cons.save()


# endregion Consumer

# region Caregiver
def add_caregiver(id: int):
    return Consumer.objects.create(account=Account.objects.get(id=id))


def has_caregiver(id):
    return Caregiver.objects.filter(account_id=id).exists()


def update_caregiver(caregiver_dto: CaregiverDto):
    care: Caregiver = Caregiver.objects.get(account_id=caregiver_dto.id)
    care.consumers = Consumer.objects.filter(pk__in=caregiver_dto.consumers)
    care.save()


def get_caregiver(caregiver_id: int) -> CaregiverDto:
    caregiver = Caregiver.objects.get(account=caregiver_id)
    dto: CaregiverDto = CaregiverDto()
    dto.id = caregiver_id
    dto.consumers = caregiver.consumers.values_list('id', flat=True)
    return dto


# endregion Caregiver

# region dispenser
def dispenser_to_dto(disp: Dispenser, consumer_id: int):
    return DispenserDto().build(
        disp.serial_num, disp.version, consumer_id, disp.registration_date, disp.obj_version)


def add_dispenser(dispenser_dto: DispenserDto):
    consumer: Consumer = None
    if dispenser_dto.consumer:
        consumer = Consumer.objects.get(account=dispenser_dto.consumer)
    return Dispenser.objects.create(
        serial_num=dispenser_dto.serial_num,
        version=dispenser_dto.version,
        consumer=consumer,
        registration_date=dispenser_dto.registration_date)


def get_dispenser(serial_num: str) -> DispenserDto:
    disp: Dispenser = Dispenser.objects.get(serial_num=serial_num)
    consumer_id = disp.consumer_id if disp.consumer else None
    return dispenser_to_dto(disp, consumer_id)


def update_dispenser(dispenser_dto: DispenserDto):
    consumer: Consumer = None
    if dispenser_dto.consumer:
        consumer = Consumer.objects.get(account=dispenser_dto.consumer)

    disp: Dispenser = Dispenser.objects.get(serial_num=dispenser_dto.serial_num)
    if disp.obj_version != dispenser_dto.obj_version:
        raise ConcurrentUpdateError()
    disp.version = dispenser_dto.version
    disp.consumer = consumer
    disp.registration_date = dispenser_dto.registration_date
    disp.save()


def get_dispensers_for_consumer_by_id(consumer_id: int) -> List[DispenserDto]:
    dispensers: List[Dispenser] = Dispenser.objects.filter(consumer=Consumer.objects.get(account_id=consumer_id))
    dips_dtos = [dispenser_to_dto(disp, consumer_id=consumer_id) for disp in dispensers]
    return dips_dtos


# endregion dispenser

# region Pod Type
def _name_to_pod_type(name: str) -> PodType:
    return PodType.objects.get(name=name)


def add_pod_type(pod_type_dto: PodTypeDto):
    pod_type = PodType.objects.create(
        name=pod_type_dto.name,
        company=Company.objects.get(business=Business.objects.get(name=pod_type_dto.company)),
        substance=pod_type_dto.substance,
        description=pod_type_dto.description,
        # capacity=pod_to_dto.capacity,
        url=pod_type_dto.url)
    return pod_type


def _pod_type_to_dto(pod_type: PodType):
    company_name = pod_type.company.business.name
    pod_dto: PodTypeDto = PodTypeDto().build(
        name=pod_type.name,
        company=company_name,
        substance=pod_type.substance,
        # pod_type.capacity,
        capacity=40,  # replace with line above when supported
        description=pod_type.description,
        url=pod_type.url
    )
    return pod_dto


def get_pod_type(pod_type_name: str) -> PodTypeDto:
    pod_type: PodType = PodType.objects.get(name=pod_type_name)
    pod_dto: PodTypeDto = _pod_type_to_dto(pod_type)
    return pod_dto


def update_pod_type(pod_type_dto: PodTypeDto):
    pod_type: PodType = PodType.objects.get(name=pod_type_dto.name)
    pod_type.name = pod_type_dto.name
    pod_type.company = Company.objects.get(name=pod_type_dto.company).pk
    pod_type.substance = pod_type_dto.substance
    pod_type.description = pod_type_dto.description
    pod_type.capacity = pod_type_dto.capacity
    pod_type.url = pod_type_dto.url
    pod_type.save()


def get_pod_types_by_company(company_name: str) -> List[PodTypeDto]:
    company: Company = Company.objects.get(name=company_name)
    pod_types: List[PodType] = PodType.objects.filter(company=company.pk)
    pod_type_dtos: List[PodDto] = [_pod_type_to_dto(pod_type) for pod_type in pod_types]
    return pod_type_dtos


# endregion Pod Type

# region Pod
def add_pod(pod_dto: PodDto, consumer_id=None):
    consumer = Consumer.objects.get(account_id=consumer_id) if consumer_id else None
    pod: Pod = Pod.objects.create(
        serial_num=pod_dto.serial_num,
        pod_type=PodType.objects.get(name=pod_dto.pod_type),
        consumer=consumer,
        remainder=pod_dto.remainder
    )
    return pod


def get_pods_for_consumer_by_id(consumer_id: int) -> List[PodDto]:
    pods: List[Pod] = Pod.objects.filter(consumer=Consumer.objects.get(account_id=consumer_id))
    pods_dtos = [pod_to_dto(pod) for pod in pods]
    return pods_dtos


def get_pod_by_serial_number(serial_number: str) -> PodDto:
    pod = Pod.objects.get(serial_num=serial_number)
    dto = pod_to_dto(pod)
    return dto


def update_pod2(pod_dto: PodDto, consumer_id: int):
    pod = Pod.objects.get(serial_num=pod_dto.serial_num)
    pod.consumer = Consumer.objects.get(account_id=consumer_id)
    pod.pod_type = PodType.objects.get(name=pod_dto.pod_type)
    pod.remainder = pod_dto.remainder
    pod.save()


def update_pod(pod_dto: PodDto, consumer_id: int):
    old_ver = pod_dto.obj_version
    new_ver = old_ver + 1
    consumer = Consumer.objects.get(account_id=consumer_id)
    updated = Pod.objects.filter(serial_num=pod_dto.serial_num, obj_version=old_ver).update(obj_version=new_ver,
                                                                                            consumer=consumer,
                                                                                            remainder=pod_dto.remainder)
    if not updated:
        found = Pod.objects.filter(serial_num=pod_dto.serial_num).exists()
        if found:
            raise ConcurrentUpdateError()
        else:
            raise ObjectDoesNotExist()


def pod_to_dto(pod):
    dto = PodDto()
    dto.pod_type = pod.pod_type.name  # get_pod_type(pod.pod_type.name)
    dto.serial_num = pod.serial_num
    dto.remainder = pod.remainder
    dto.obj_version = pod.obj_version
    return dto


# endregion Pod


# region Dosing
def _dosing_to_dto(dosing: Dosing):
    # dto = DosingDto.build(
    #     dosing.id,
    #     dosing.pod.serial_num,
    #     dosing.time,
    #     dosing.amount,
    #     dosing.latitude,
    #     dosing.longitude
    # )
    dto = DosingDto()
    dto.dosing_id = dosing.id
    dto.pod = dosing.pod.serial_num
    dto.time = dosing.time
    dto.amount = dosing.amount
    dto.latitude = dosing.latitude
    dto.longitude = dosing.longitude

    return dto


def add_dosing(dosing_dto: DosingDto):
    Dosing.objects.create(
        pod=Pod.objects.get(serial_num=dosing_dto.pod),
        time=dosing_dto.time,
        amount=dosing_dto.amount,
        latitude=dosing_dto.latitude,
        longitude=dosing_dto.longitude
    )


def get_dosings_for_consumer_by_id(consumer_id: int) -> List[DosingDto]:
    pods: List[Pod] = Pod.objects.filter(consumer=Consumer.objects.get(account=consumer_id))
    dosings: List[Dosing] = Dosing.objects.filter(pod__in=pods)
    return [_dosing_to_dto(dosing) for dosing in dosings]


def get_dosings_for_pod(pod_serial_num: str) -> List[DosingDto]:
    dosings: List[Dosing] = Dosing.objects.filter(pod=Pod.objects.get(serial_num=pod_serial_num))
    return [_dosing_to_dto(dosing) for dosing in dosings]


# endregion Dosing


# region Regimen
def _regimen_entry_to_tuple(entry: Regimen):
    return (entry.pod_type.name, entry.day, entry.time, entry.amount)


def delete_regimens(consumer_id):
    consumer = Consumer.objects.get(account=consumer_id)
    Regimen.objects.filter(consumer=consumer).delete()


# type,day,time,amount
# model -consumer, pod_type, day, time, amount
def add_to_regimen_with_id(consumer_id: int, pod_type_name: str, day: int, time: int, amount: float):
    Regimen.objects.create(
        consumer=_id_to_consumer(consumer_id),
        pod_type=_name_to_pod_type(pod_type_name),
        day=day,
        time=time, amount=amount
    )


# podType -> (day, time) -> ammount
def get_regimen_by_consumer_id(consumer_id: int) -> RegimenDto:
    # RegimenDto reg_dto = RegimenDto()
    entries: List[Regimen] = Regimen.objects.filter(consumer=_id_to_consumer(consumer_id))
    return [_regimen_entry_to_tuple(entry) for entry in entries]


# endregion Regimen


# region Feedback
# dosing, rating, comment
def _feedback_to_dto(feedback: Feedback) -> FeedbackDto:
    return FeedbackDto().build(
        feedback.id,
        feedback.dosing.id,
        feedback.rating,
        feedback.time,
        feedback.comment
    )


def add_feedback(feedback_dto: FeedbackDto):
    Feedback.objects.create(
        dosing=Dosing.objects.get(id=feedback_dto.dosing_id),
        rating=feedback_dto.rating,
        time=feedback_dto.time,
        comment=feedback_dto.comment
    )


def get_feedbacks_for_consumer(consumer_id: int) -> List[FeedbackDto]:
    pods: List[Pod] = Pod.objects.filter(consumer=Consumer.objects.get(account=consumer_id))
    dosings: List[Dosing] = Dosing.objects.filter(pod__in=pods)
    feedbacks: List[Feedback] = Feedback.objects.filter(dosing__in=dosings)
    return [_feedback_to_dto(feedback) for feedback in feedbacks]


def get_feedback_for_dosing(dosing_id: int) -> FeedbackDto:
    feedback = Feedback.objects.get(dosing=Dosing.objects.get(id=dosing_id))
    dto = _feedback_to_dto(feedback)
    return dto


# endregion Feedback


# region Feedback Reminder
# dosing, time
def _feedback_reminder_to_dto(feedback_reminder: FeedbackReminder) -> FeedbackReminderDto:
    return FeedbackReminderDto().build(
        feedback_reminder.dosing.id,
        feedback_reminder.time
    )


def add_feedback_reminder(feedback_reminder_dto: FeedbackReminderDto):
    FeedbackReminder.objects.create(
        dosing=Dosing.objects.get(id=feedback_reminder_dto.dosing),
        time=feedback_reminder_dto.time
    )


# todo: implement
def get_all_feedback_reminders_in_time_window(from_time, until_time) -> List[FeedbackReminderDto]:
    return []


# endregion Feedback Reminder

def add_company(business_name: str):
    Business.objects.create(name=business_name, docs_path="/")
    company = Company.objects.create(business=Business.objects.get(name=business_name))
    return company
