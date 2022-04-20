from django.contrib.auth.models import User
from django_site.accounts.models import Account
from django_site.consumer_app.models import Consumer

def add_account(email, pwd, phone, f_name, l_name, dob):
    User.objects.create_user(email, email, pwd)
    account = Account.objects.create(email=email, f_name=f_name, l_name=l_name, phone=phone, dob=dob)    
    return account

def get_account_by_email(email: str) -> Account:
    return Account.objects.get(email=email)

def get_account_by_id(id: int) -> Account:
    return Account.objects.get(id=id)


def add_consumer(id: int, residence:str, height:int, weight:int, units: str, gender:str, goal:any):
    return Consumer.objects.create(
        account=id, residence=residence, height=height, weight=weight, 
        units=units, gender=gender, goal=goal
    )