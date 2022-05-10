import asyncio

from voyager_system.domain.medical_center.Consumer import Consumer


class IMapper:
    # class attribute

    # instance init
    def __init__(self):
        pass

    # methods
    async def get_consumer(self,consumer_id):
        raise NotImplementedError("Should have implemented this")


    async def add_consumer(self, consumer: Consumer):
        raise NotImplementedError("Should have implemented this")


    async def update_consumer(self,consumer: Consumer):
        raise NotImplementedError("Should have implemented this")


    async def delete_consumer(self,consumer: Consumer):
        raise NotImplementedError("Should have implemented this")

    #general user
    async def add_account(self, email: str, f_name: str, l_name: str, phone: str, pwd: str):
        raise NotImplementedError("Should have implemented this")

    async def get_account(self, email: str):
        raise NotImplementedError("Should have implemented this")

    async def get_account_by_id(self, user_id: int):
        raise NotImplementedError("Should have implemented this")
