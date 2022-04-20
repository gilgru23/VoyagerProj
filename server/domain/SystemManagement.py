import re
import domain.common.Result as res
from server.dal.DummyMapper import DummyMapper
from server.dal.IMapper import IMapper

from server.domain.medicalCenter.MedicalCenter import MedicalCenter
import data_access.database as db

EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

#todo: handle phone number and password
def create_account(email: str, f_name: str, l_name: str, phone: str, pwd: str) -> str:
    if not re.search(EMAIL_REGEX, email):
        return res.failure("Invalid email format")
    if (not f_name) or (not l_name):
        return res.failure("Invalid name")
    if is_email_registerred(email):
        return res.failure("email already registerred")
    db.add_account
    return True

def create_consumer_profile(id: int, residence:str, height:int, weight:int, units: str, gender:str, goal:any):
    if not does_id_exist(id):
        return res.failure("no associated account")
    if is_consumer(id):
        return res.failure("already a consumer")
    #todo: validate other fields
    return db.add_consumer(id, residence, height, weight, units, gender, goal)


def is_email_registerred(email):
    return False

def does_id_exist(id: int) -> bool:
    return False

def is_consumer(id: int) -> bool:
    return False


class SystemManagement:
    def __init__(self) -> None:
        self.med_center = MedicalCenter()
        self.object_mapper: IMapper = DummyMapper()
        

    async def login(self, email: str, pwd: str) -> str:
        account = await self.object_mapper.get_account(email)
        if not account:
            return res.failure("email not found")
        if account.pwd != pwd:
            return res.failure("incorrect password")
        return res.success(account)

    async def register_as_consumer(self, user_id: int) -> str:
        account = await self.object_mapper.get_account_by_id(user_id)
        if not account:
            return res.failure("user not found")
        return await self.med_center.register_consumer(user_id)


    