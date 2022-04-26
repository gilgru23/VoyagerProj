from accounts.models import Account
from consumer_app.models import Consumer, Dispenser

from voyager_system.data_access.dtos import AccountDto, ConsumerDto, DispenserDto

#region Account
def has_account_with_email(email):
    return Account.objects.filter(email=email).exists()

def add_account(email, f_name, l_name, phone, dob):
    account = Account.objects.create(email=email, f_name=f_name, l_name=l_name, phone=phone, dob=dob)    
    return account

def add_account(acct_dto: AccountDto):
    # email, phone, f_name, l_name, dob
    account = Account.objects.create(
        email=acct_dto.email, f_name=acct_dto.f_name, l_name=acct_dto.l_name, phone=acct_dto.phone, dob=acct_dto.dob
    )    
    return account

def get_account_by_email(email: str) -> Account:
    return Account.objects.get(email=email)

def get_account_by_id(id: int) -> Account:
    return Account.objects.get(id=id)

def update_account(acct_dto: AccountDto):
    acct: Account = Account.objects.get(id = acct_dto.id)
    acct.email = acct_dto.email
    acct.phone = acct_dto.phone
    acct.f_name = acct_dto.f_name
    acct.l_name = acct_dto.l_name
    acct.phone = acct_dto.phone
    acct.save()
#endregion Account

#region Consumer
def add_consumer(id: int, residence:str, height:int, weight:int, units: str, gender:str, goal:any):
    return Consumer.objects.create(
        account=Account.objects.get(id=id),
        residence=residence, height=height, weight=weight, 
        units=units, gender=gender#, goal=goal
    )

def get_consumer(account_id: int) -> Consumer:
    return Consumer.objects.get(account = account_id)

def update_consumer(consumer_dto: ConsumerDto):
    cons: Consumer = Consumer.objects.get(account=consumer_dto.account)
    cons.residence = consumer_dto.residence
    cons.height = consumer_dto.height
    cons.weight = consumer_dto.weight
    cons.units = consumer_dto.units
    cons.gender = consumer_dto.gender
    cons.goal = consumer_dto.goal
    cons.save()
    
#dispenser
def add_dispenser(serial_num: str, version: str):
    return Dispenser.objects.create(serial_num=serial_num, version=version)

def get_dispenser(serial_num: str) -> Dispenser:
    return Dispenser.objects.get(serial_num=serial_num)

#todo: depreciate, use update_dispenser instead
def set_dispenser_consumer(serial_num: str, consumer_id: int):
    dispenser = Dispenser.objects.get(serial_num=serial_num)
    dispenser.consumer_id = consumer_id
    dispenser.save()

def update_dispenser(dispenser_dto: DispenserDto):
    disp: Dispenser = Dispenser.objects.get(serial_num=dispenser_dto.serial_num)

    disp.version = dispenser_dto.version
    disp.consumer = dispenser_dto.consumer
    disp.registration_date = dispenser_dto.registration_date
    disp.save()
#endregion Consumer