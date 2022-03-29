

class GuestService:
    def __init__(self) -> None:
        pass

    async def create_account(self, email: str, first_name: str, last_name: str, phone_num: str, pwd: str) -> str:
        pass

    async def login(self, email: str, pwd: str) -> str:
        pass

    async def register_as_consumer(self, email: str) -> str:
        pass