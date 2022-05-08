from voyager_system.data_access.dtos import ConsumerDto, DispenserDto
from voyager_system.data_access.dtos import AccountDto
import voyager_system.data_access.database as db

SUFFIX = '13'
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


def foo():
    db.add_account(EMAIL, F_NAME, L_NAME, PHONE, DOB)
    assert_account(EMAIL, F_NAME, L_NAME, PHONE, DOB)

    acct_dto: AccountDto = db.get_account_by_email(EMAIL)
    acct_id = acct_dto.id
    
    db.add_consumer(acct_id, RESIDENCE, HEIGHT, WEIGHT, UNITS, GENDER, GOAL)
    assert_consumer(acct_id, RESIDENCE, HEIGHT, WEIGHT, UNITS, GENDER, GOAL)

    dispenser_dto = DispenserDto().build(DISPENSER_SERIAL_NUM, DISPENSER_VERSION, None, None)
    db.add_dispenser(dispenser_dto)
    assert_dispenser(dispenser_dto)

    dispenser_dto.build(DISPENSER_SERIAL_NUM, DISPENSER_VERSION, acct_id, DISPENSER_REG_DATE)
    db.update_dispenser(dispenser_dto)
    assert_dispenser(dispenser_dto)

    


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
    except:
        print('failed on assert_account')

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
    except:
        print('failed on assert_consumer')


def assert_dispenser(disp_dto: DispenserDto):
    try:
        disp_dto_2: DispenserDto = db.get_dispenser(disp_dto.serial_num)
        assert disp_dto_2.serial_num == disp_dto.serial_num
        assert disp_dto_2.consumer == disp_dto.consumer
        assert disp_dto_2.version == disp_dto.version
        assert disp_dto_2.registration_date == disp_dto.registration_date
    except:
        print('failed on assert_dispenser')