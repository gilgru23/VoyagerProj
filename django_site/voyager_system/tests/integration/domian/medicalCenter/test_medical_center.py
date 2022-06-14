import unittest

from voyager_system.common.ErrorTypes import AppOperationError
from voyager_system.tests.test_objects.DummyMapper import DummyMapper
from voyager_system.data_access.DatabaseProxy import *
from voyager_system.tests.test_objects.DummyDatabase import DummyDatabase
from voyager_system.domain.medical_center.Consumer import Consumer
from voyager_system.domain.medical_center.Dosing import Dosing
from voyager_system.domain.medical_center.MedicalCenter import MedicalCenter
from voyager_system.domain.medical_center.Pod import *


class TestMedicalCenter(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        super(TestMedicalCenter, self).__init__(*args, **kwargs)
        self.test_mapper = DummyMapper(consumer_factory=consumer_factory)
        self.test_db = DummyDatabase(consumer_factory=consumer_factory)
        self.medical_center = MedicalCenter(db_proxy=DatabaseProxy(self.test_db))

    def setUp(self):
        print('\nset up integration test')
        self.test_mapper.consumer_factory = consumer_factory
        self.test_db = consumer_factory
        pass

    def tearDown(self):
        print('tear down integration test')
        pass

    async def test_get_consumer_success(self):
        print(f'Test: get consumer - success')
        consumer_id = 1
        consumer = await self.medical_center.get_consumer(consumer_id)
        self.assertTrue(consumer)
        real_consumer = consumer_factory(consumer_id)
        for pod1, pod2 in zip(consumer.pods, real_consumer.pods):
            self.assertEqual(pod1.id, pod2.id)
        for dosing1, dosing2 in zip(consumer.dosing_history, real_consumer.dosing_history):
            self.assertEqual(dosing1.id, dosing2.id)

    async def test_get_consumer_fail_1(self):
        print(f'Test: get consumer - fail 1')
        print(f'\tno consumer with the given id in the system')
        self.test_db.consumer_factory = consumer_factory_bad
        self.test_mapper.consumer_factory = consumer_factory_bad

        with self.assertRaises(AppOperationError):
            await self.medical_center.get_consumer(1)
        pass

    async def test_get_consumer_fail_2(self):
        print(f'Test: get consumer - fail 2')
        print(f'\tno connection with DB')
        self.test_db.consumer_factory = consumer_factory_broken
        self.test_mapper.consumer_factory = consumer_factory_broken

        with self.assertRaises(AppOperationError):
            await self.medical_center.get_consumer(1)
        pass

    async def test_get_consumer_dosing_history(self):
        print(f'Test: get consumer dosing history')
        consumer_id = 1
        history = await self.medical_center.get_consumer_dosing_history(consumer_id)
        self.assertTrue(history is not None)
        real_history = await consumer_factory(consumer_id).get_dosage_history()
        for dose1, dose2 in zip(history, real_history):
            self.assertEqual(dose1.id, dose2.id)

    async def test_get_consumer_pods(self):
        print(f'Test: get consumer pods')
        consumer_id = 1
        pods = self.medical_center.get_consumer_pods(consumer_id)
        self.assertTrue(pods is not None)
        real_pods = consumer_factory(consumer_id).get_pods()
        for pod1, pod2 in zip(pods, real_pods):
            self.assertEqual(pod1.pod_serial_number, pod2.serial_number)

    async def test_consumer_dose_success(self):
        print(f'Test: consumer dose - success')
        consumer_id = 1
        consumer1 = consumer_factory(consumer_id)
        self.test_db.consumer_factory = lambda i: consumer1
        self.test_mapper.consumer_factory = lambda i: consumer1
        pod_id = 1
        amount = 42.5
        await self.medical_center.consumer_dose(consumer_id=consumer_id, pod_id=pod_id, amount=amount, location='here')

        real_pod = await consumer1.get_pod_by_id(pod_id)
        self.assertEqual(real_pod.remainder, 100 - amount)
        real_dosing = consumer1.dosing_history[0]
        self.assertEqual(real_dosing.amount, amount)
        self.assertEqual(real_dosing.pod_serial_number, pod_id)


    async def test_consumer_dose_fail_1(self):
        print(f'Test: consumer dose - fail 1')
        print(f'\tno pods to dose from')
        consumer_id = 1
        consumer1 = consumer_factory(consumer_id)
        self.test_db.consumer_factory = lambda i: consumer1
        self.test_mapper.consumer_factory = lambda i: consumer1
        consumer1.pods = []
        with self.assertRaises(AppOperationError):
            await self.medical_center.consumer_dose(consumer_id=consumer_id, pod_id=1, amount=42.5, location='here')


    async def test_consumer_dose_fail_2(self):
        print(f'Test: consumer dose - fail 2')
        print(f'\tincorrect pod id')
        with self.assertRaises(AppOperationError):
            await self.medical_center.consumer_dose(consumer_id=1, pod_id=1000, amount=42.5, location='here')

    async def test_consumer_dose_fail_3(self):
        print(f'Test: consumer dose - fail 3')
        print(f'\tdosing amount too large')
        with self.assertRaises(AppOperationError):
            await self.medical_center.consumer_dose(consumer_id=1, pod_id=1, amount=1000, location='here')

# helper methods and factories
def consumer_factory(consumer_id):
    consumer = Consumer()
    consumer.id = consumer_id
    pod_type_1 = PodType(type_id=111, capacity=100, description="None")
    dosings = [Dosing(dosing_id=i, pod_id=i // 2, pod_type_id=pod_type_1.type_id, amount=20, time=None, location=None)
               for i in range(10)]
    pods = [Pod(pod_id=i, pod_type=pod_type_1) for i in range(5)]
    consumer.dosing_history = dosings
    consumer.pods = pods
    print(f"Here is consumer #{consumer_id}!")
    return consumer


def consumer_factory_bad(consumer_id):
    print(f"consumer #{consumer_id} was not found! )-:")
    return None


def consumer_factory_broken(consumer_id):
    print(f"no connection to DB! )-:")
    raise DataAccessError('This is a test error. should be caught')


if __name__ == '__main__':
    unittest.main()
