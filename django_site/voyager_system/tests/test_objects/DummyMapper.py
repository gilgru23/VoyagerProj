import asyncio
from voyager_system.dal.IMapper import IMapper
from voyager_system.domain.medicalCenter.Consumer import *


class DummyMapper(IMapper):

    # instance init
    def __init__(self, consumer_factory):
        super(DummyMapper, self).__init__()
        self.consumer_factory = consumer_factory

    @staticmethod
    def consumer_error(consumer_id):
        return False, f"Error : consumer [{consumer_id}] not found!"

    # methods
    async def get_consumer(self,consumer_id):
        print("DummyMapper: get_consumer was called")
        print(f"Here is consumer #{consumer_id}!")

        # failure example
        # if False:
        #     self.consumer_error(consumer_id)

        return self.consumer_factory(consumer_id)


    async def add_consumer(self,consumer_id):
        print("DummyMapper: add_consumer was called!")


    async def update_consumer(self,consumer):
        print("DummyMapper: update_consumer was called!")


    async def delete_consumer(self,consumer):
        print("DummyMapper: delete_consumer was called!")

    #general user
    async def add_account(self, email: str, f_name: str, l_name: str, phone: str, pwd: str):
        print("DummyMapper: add_account was called!")

    async def get_account(self, email: str):
        print("DummyMapper: get_account was called!")

    async def get_account_by_id(self, user_id: int):
        print("DummyMapper: get_account_by_id was called!")
