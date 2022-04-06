import re
import domain.common.Result as res
from server.dal.DummyMapper import DummyMapper
from server.dal.IMapper import IMapper

from server.domain.medicalCenter.MedicalCenter import MedicalCenter

EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

class SystemManagement:
    def __init__(self) -> None:
        self.med_center = MedicalCenter()
        self.object_mapper: IMapper = DummyMapper()
        

    #todo: handle phone number and password
    async def create_account(self, email: str, f_name: str, l_name: str, phone: str, pwd: str) -> str:
        if not re.search(EMAIL_REGEX, email):
            return res.failure("Invalid email format")
        if (not f_name) or (not l_name):
            return res.failure("Invalid name")
        if await self.object_mapper.get_account(email):
            return res.failure("email already registerred")

        #todo: store in db
        return None

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


    