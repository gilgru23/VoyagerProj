from dal.IMapper import IMapper
from dal.MockCacher import MockCacher
from dal.Util import DataAccessError
from dal.db.DBController import *


class MockMapper(IMapper):
    # class attribute
    db = DBController()
    cache = MockCacher()

    # instance init
    def __init__(self):
        super(MockMapper, self).__init__()


    @staticmethod
    def consumer_error(consumer_id):
        return False, f"Error : consumer [{consumer_id}] not found!"

    # methods
    async def get_consumer(self,consumer_id):
        consumer = await self.cache.get_consumer_by_id(consumer_id=consumer_id)
        if consumer:
            return consumer
        consumer = await self.db.get_consumer(consumer_id=consumer_id)
        if consumer:
            await self.cache.add_consumer_to_cache(consumer)
            return consumer
        return None


    async def add_consumer(self,consumer: Consumer):
        # @TODO: check if there is already a consumer woth same email(?)
        await self.db.add_consumer(consumer)
        await self.cache.add_consumer_to_cache(consumer)


    async def update_consumer(self,consumer):
        print("MockMapper (Dummy): update_consumer was called!")


    async def delete_consumer(self,consumer):
        print("MockMapper (Dummy): delete_consumer was called!")

    # general user
    async def add_account(self, email: str, f_name: str, l_name: str, phone: str, pwd: str):
        print("MockMapper (Dummy): add_account was called!")


    async def get_account(self, email: str):
        print("MockMapper (Dummy): get_account was called!")


    async def get_account_by_id(self, user_id: int):
        print("MockMapper (Dummy): get_account_by_id was called!")