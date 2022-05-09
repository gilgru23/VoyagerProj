import random
from typing import List
from voyager_system.data_access.dtos import ConsumerDto, DispenserDto, PodDto, PodTypeDto, AccountDto
import voyager_system.data_access.database as db

SUFFIX = str(random.randint(111, 28937492923432))
EMAIL = 'tbaby' + SUFFIX +'@blah.com'
PWD = 'dshkjkKJHDU365#@'
PHONE = '123'
F_NAME = 'John'
L_NAME = 'Doe'
DOB = '1993-06-12'

RESIDENCE = '12345'
HEIGHT = 12
WEIGHT = 10
UNITS = 1
GENDER = 1
GOAL = None

DISPENSER_SERIAL_NUM = 'ksjjn323lk' + SUFFIX
DISPENSER_VERSION = 'v1'
DISPENSER_REG_DATE = '2022-01-01'

COMPANY_NAME = 'Area 51 ' + SUFFIX
POD_SERIAL_NUM = 'kdjfnker' + SUFFIX
POD_TYPE_NAME = 'Charlettes Web ' + SUFFIX
SUBSTANCE = 'That Good Good'
CAPCITY = 50
DESCRIPTION = 'Meet your better self'
URL = 'www.area51.com/charlotte'


def update_uniques():
    global SUFFIX, EMAIL, DISPENSER_SERIAL_NUM, POD_SERIAL_NUM, POD_TYPE_NAME, COMPANY_NAME
    SUFFIX = str(random.randint(111, 28937492923432))
    EMAIL = 'tbaby' + SUFFIX +'@blah.com'
    DISPENSER_SERIAL_NUM = 'ksjjn323lk' + SUFFIX
    POD_SERIAL_NUM = 'kdjfnker' + SUFFIX
    POD_TYPE_NAME = 'Charlettes Web ' + SUFFIX
    COMPANY_NAME = 'Area 51 ' + SUFFIX



def foo():
    #signing up
    update_uniques()
    db.add_account(EMAIL, F_NAME, L_NAME, PHONE, DOB)
    assert_account(EMAIL, F_NAME, L_NAME, PHONE, DOB)

    acct_dto: AccountDto = db.get_account_by_email(EMAIL)
    acct_id = acct_dto.id
    
    db.add_consumer(acct_id, RESIDENCE, HEIGHT, WEIGHT, UNITS, GENDER, GOAL)
    assert_consumer(acct_id, RESIDENCE, HEIGHT, WEIGHT, UNITS, GENDER, GOAL)

    #dispenser
    dispenser_dto = DispenserDto().build(DISPENSER_SERIAL_NUM, DISPENSER_VERSION, None, None)
    db.add_dispenser(dispenser_dto)
    assert_dispenser(dispenser_dto)

    dispenser_dto.build(DISPENSER_SERIAL_NUM, DISPENSER_VERSION, acct_id, DISPENSER_REG_DATE)
    db.update_dispenser(dispenser_dto)
    assert_dispenser(dispenser_dto)

    #pod
    db.add_company(COMPANY_NAME)
    pod_type_dto : PodTypeDto = PodTypeDto().build(POD_TYPE_NAME, COMPANY_NAME, SUBSTANCE, CAPCITY, DESCRIPTION, URL)
    db.add_pod_type(pod_type_dto)
    assert_pod_type(pod_type_dto)
    
    pod_dto: PodDto = PodDto().build(POD_SERIAL_NUM, POD_TYPE_NAME, CAPCITY)
    db.add_pod(pod_dto, acct_id)
    assert_pod(pod_dto, acct_id)

    


def assert_account(email, f_name, l_name, phone, dob):
    try:
        assert db.has_account_with_email(email)
        acct_dto : AccountDto = db.get_account_by_email(email)
        assert db.has_account_with_id(acct_dto.id)
        assert acct_dto.email == email
        assert acct_dto.f_name == f_name
        assert acct_dto.l_name == l_name
        # assert acct_dto.phone == phone
        # assert acct_dto.dob == dob
    except Exception as e:
        print('failed on assert_account\n' + str(e))

def assert_consumer(acct_id, residence, height, weight, units, gender, goal):
    try:
        cons_dto: ConsumerDto = db.get_consumer(acct_id)
        assert cons_dto.id == acct_id
        assert cons_dto.residence == residence
        assert cons_dto.height == height
        assert cons_dto.weight == weight
        assert cons_dto.units == units
        assert cons_dto.gender == gender
        assert cons_dto.goal == goal
    except Exception as e:
        print('failed on assert_consumer\n' + str(e))

def assert_dispenser(disp_dto: DispenserDto):
    try:
        disp_dto_2: DispenserDto = db.get_dispenser(disp_dto.serial_num)
        assert disp_dto_2.serial_num == disp_dto.serial_num
        assert disp_dto_2.consumer == disp_dto.consumer
        assert disp_dto_2.version == disp_dto.version
        # assert disp_dto_2.registration_date == disp_dto.registration_date
    except Exception as e:
        print('failed on assert_dispenser\n' + str(e))

def assert_pod_type(pod_type_dto: PodTypeDto):
    try:
        other : PodTypeDto = db.get_pod_type(pod_type_dto.name)
        assert other.name == pod_type_dto.name
        assert other.company == pod_type_dto.company
        assert other.substance == pod_type_dto.substance
        assert other.capacity == pod_type_dto.capacity
        assert other.description == pod_type_dto.description
        assert other.url == pod_type_dto.url
    except Exception as e:
        print('failed on assert_pod_type\n' + str(e))

def assert_pod(pod_dto : PodDto, acct_id):
    try:
        pods : List[PodDto] = db.get_pods_for_consumer_by_id(acct_id)
        assert len(pods) == 1
        other : PodDto = pods[0]
        assert other.serial_num == pod_dto.serial_num
        assert other.pod_type == pod_dto.pod_type
        assert other.remainder == pod_dto.remainder
    except Exception as e:
        print('failed on assert_pod\n' + str(e))  