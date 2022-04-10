from dal.IMapper import IMapper
from dal.MockCacher import MockCacher
from domain.medicalCenter.Consumer import *
from dal.orm.DBController import *


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
        consumer_res = await self.cache.get_consumer_by_id(consumer_id=consumer_id)
        if Res.is_successful(consumer_res):
            return Res.get_value(consumer_res)
        consumer_res = await self.db.get_consumer(consumer_id=consumer_id)
        if Res.is_successful(consumer_res):
            consumer = Res.get_value(consumer_res)
            add_consumer_res = await self.cache.add_consumer_to_cache(consumer)
            if Res.is_successful(add_consumer_res):
                return Res.get_value(consumer)
            else:
                return add_consumer_res
        return consumer_res


    async def add_consumer(self,consumer: Consumer):
        get_cache_res = await self.cache.get_consumer_by_id(consumer_id=consumer.id)
        if Res.is_failure(get_cache_res):
            return get_cache_res
        add_db_res = await self.db.add_consumer(consumer)
        if Res.is_failure(add_db_res):
            return add_db_res
        add_cache_res = await self.cache.add_consumer_to_cache(consumer)
        if Res.is_failure(add_cache_res):
            return add_cache_res
        return Res.success()


    async def update_consumer(self,consumer):
        print("MockMapper (Dummy): update_consumer was called!")


    async def delete_consumer(self,consumer):
        print("MockMapper (Dummy): delete_consumer was called!")

    #general user
    async def add_account(self, email: str, f_name: str, l_name: str, phone: str, pwd: str):
        print("MockMapper (Dummy): add_account was called!")

    async def get_account(self, email: str):
        print("MockMapper (Dummy): get_account was called!")

    async def get_account_by_id(self, user_id: int):
        print("MockMapper (Dummy): get_account_by_id was called!")