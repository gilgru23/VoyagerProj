

from server.domain.SystemManagement import SystemManagement


class GuestService:
    def __init__(self) -> None:
        self.system_management = SystemManagement()
        pass

    async def create_account(self, email: str, first_name: str, last_name: str, phone_num: str, pwd: str) -> str:
        return self.system_management.create_account(email, first_name, last_name, phone_num, pwd)

    async def login(self, email: str, pwd: str) -> str:
        return self.system_management.login(email, pwd)

    async def register_as_consumer(self, user_id: int) -> str:
        pass