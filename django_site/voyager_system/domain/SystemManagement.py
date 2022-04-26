import re
import voyager_system.domain.common.Result as res

from voyager_system.domain.medicalCenter.MedicalCenter import MedicalCenter
from voyager_system.data_access.DatabaseProxy import DatabaseProxy


#
# EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
#
# #todo: handle phone number and password
# def create_account(email, phone, f_name, l_name, dob) -> str:
#     if not re.search(EMAIL_REGEX, email):
#         return res.failure("Invalid email format")
#     if not (email and phone and f_name and l_name and dob):
#         return res.failure("Invalid parameters")
#     if is_email_registerred(email):
#         return res.failure("email already registerred")
#     db.add_account(email, phone, f_name, l_name, dob)
#     return res.success()
#
# def create_consumer_profile(id: int, residence:str, height:int, weight:int, units: str, gender:str, goal:any):
#     if not does_id_exist(id):
#         return res.failure("no associated account")
#     if is_consumer(id):
#         return res.failure("already a consumer")
#     #todo: validate other fields
#     return db.add_consumer(id, residence, height, weight, units, gender, goal)
#
#
# def is_email_registerred(email):
#     return db.has_account_with_email(email)
#
# def does_id_exist(id: int) -> bool:
#     return True
#
# def is_consumer(id: int) -> bool:
#     return False


class SystemManagement:

    def __init__(self, medical_center: MedicalCenter, db_proxy: DatabaseProxy) -> None:
        self.med_center: MedicalCenter = medical_center
        self.db_proxy: DatabaseProxy = db_proxy

    async def login(self, email: str, pwd: str) -> str:
        account = await self.db_proxy.get_account(email)
        if not account:
            return res.failure("email not found")
        if account.pwd != pwd:
            return res.failure("incorrect password")
        return res.success(account)

    async def register_as_consumer(self, user_id: int) -> str:
        account = await self.db_proxy.get_account_by_id(user_id)
        if not account:
            return res.failure("user not found")
        return await self.med_center.register_consumer(user_id)

    EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    # todo: handle phone number and password
    def create_account(self, email, phone, f_name, l_name, dob) -> str:
        if not re.search(self.EMAIL_REGEX, email):
            return res.failure("Invalid email format")
        if not (email and phone and f_name and l_name and dob):
            return res.failure("Invalid parameters")
        if self.is_email_registered(email):
            return res.failure("email already registered")
        self.db_proxy.add_account(email, phone, f_name, l_name, dob)
        return res.success()

    def create_consumer_profile(self, id: int, residence: str, height: int, weight: int, units: str, gender: str,
                                goal: any):
        if not self.does_id_exist(id):
            return res.failure("no associated account")
        if self.is_consumer(id):
            return res.failure("already a consumer")
        # todo: validate other fields
        return self.db_proxy.add_consumer(id, residence, height, weight, units, gender, goal)

    def is_email_registered(self, email):
        return self.db_proxy.has_account_with_email(email)

    def does_id_exist(self, id: int) -> bool:
        return True

    def is_consumer(self, id: int) -> bool:
        return False
