import asyncio

from dal.IMapper import IMapper


class DummyMapper(IMapper):
    # class attribute
    engine = None
    session = None

    # instance init
    def __init__(self):
        super(DummyMapper, self).__init__()


    # methods
    async def get_consumer(self,consumer_id):
        print("DummyMapper: get_consumer was called!")
        print(f"here is consumer #{consumer_id}!")


    async def add_consumer(self,consumer_id):
        print("DummyMapper: add_consumer was called!")


    async def update_consumer(self,consumer):
        print("DummyMapper: update_consumer was called!")


    async def delete_consumer(self,consumer):
        print("DummyMapper: delete_consumer was called!")
