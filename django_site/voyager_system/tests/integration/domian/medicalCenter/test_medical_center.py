import unittest
from voyager_system.dal.DummyMapper import DummyMapper
from voyager_system.data_access.DatabaseProxy import *
from voyager_system.data_access.DummyDatabase import DummyDatabase
from voyager_system.domain.medicalCenter.Consumer import Consumer
from voyager_system.domain.medicalCenter.Dosing import Dosing
from voyager_system.domain.medicalCenter.MedicalCenter import MedicalCenter
from voyager_system.domain.medicalCenter.Pod import *


class TestMedicalCenter(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        super(TestMedicalCenter, self).__init__(*args, **kwargs)
        self.test_mapper = DummyMapper(consumer_factory=consumer_factory)
        dummy_db = DummyDatabase(consumer_factory=consumer_factory)
        self.medical_center = MedicalCenter(mapper=self.test_mapper, db_proxy=DatabaseProxy(dummy_db))

    def setUp(self):
        pass

    async def test_example(self):
        await self.medical_center.get_consumer(1)
        self.assertTrue(True)


    async def test_0_consumer_get_dosing_history(self):
        consumer = await self.medical_center.get_consumer(1)
        self.assertTrue(consumer is not None)
        history = await consumer.get_dosage_history()
        self.assertTrue(history is not None)


def consumer_factory(consumer_id):
    consumer = Consumer()
    consumer.id = consumer_id
    dosings = [Dosing(dosing_id=i, pod_id=i // 2, amount=20, time=None, location=None) for i in range(10)]
    pod_type_1 = PodType(type_id=111, capacity=100, description="None")
    pods = [Pod(pod_id=i, pod_type=pod_type_1) for i in range(5)]
    consumer.dosing_history = dosings
    consumer.pods = pods
    return consumer