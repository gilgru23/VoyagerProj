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
        print("DummyMapper: get_consumer was called")
        print(f"Here is consumer #{consumer_id}!")

        # failure example
        # if False:
        #     self.consumer_error(consumer_id)

        consumer = Consumer()
        consumer.id = consumer_id
        dosings = [Dosing(dosing_id=i, pod_id=i//2, amount=20, time=None, location=None) for i in range(10)]
        pod_type_1 = PodType(type_id=111, capacity=100, description="None")
        pods = [Pod(pod_id=i,pod_type=pod_type_1) for i in range(5)]
        consumer.dosing_history = dosings
        consumer.pods = pods
        return Res.success(consumer)


    async def add_consumer(self,consumer_id):
        print("MockMapper (Dummy): add_consumer was called!")


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