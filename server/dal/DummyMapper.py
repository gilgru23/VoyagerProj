import asyncio

from dal.IMapper import IMapper
from domain.medicalCenter.Consumer import Consumer


class DummyMapper(IMapper):
    # class attribute
    engine = None
    session = None

    # instance init
    def __init__(self):
        super(DummyMapper, self).__init__()


    # methods
    async def get_consumer(self,consumer_id):
        print("DummyMapper: get_consumer was called")
        print(f"Here is consumer #{consumer_id}!")
        consumer = Consumer()
        consumer.id = consumer_id
        return consumer


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
