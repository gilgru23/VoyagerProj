from django.contrib.auth.models import User
from accounts.models import Account
from consumer_app.models import Consumer, Dispenser

#region Account
def has_account_with_email(email):
    return Account.objects.filter(email=email).exists()

def add_account(email, phone, f_name, l_name, dob):
    account = Account.objects.create(email=email, f_name=f_name, l_name=l_name, phone=phone, dob=dob)    
    return account

def get_account_by_email(email: str) -> Account:
    return Account.objects.get(email=email)

def get_account_by_id(id: int) -> Account:
    return Account.objects.get(id=id)
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

def add_dispenser(serial_num: str, version: str):
    return Dispenser.objects.create(serial_num=serial_num, version=version)

def get_dispender(serial_num: str) -> Dispenser:
    return Dispenser.objects.get(serial_num=serial_num)

def set_dispenser_consumer(serial_num: str, consumer_id: int):
    dispenser = Dispenser.objects.get(serial_num=serial_num)
    dispenser.consumer_id = consumer_id
    dispenser.save()

#endregion Consumer