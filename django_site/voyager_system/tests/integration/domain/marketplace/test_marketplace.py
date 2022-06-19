from django.test import TestCase

from django.utils import timezone
from voyager_system.common.DateTimeFormats import parse_string_to_timezone

from voyager_system.common.ErrorTypes import AppOperationError
from voyager_system.tests.test_objects.DummyMapper import DummyMapper
from voyager_system.data_access.DatabaseProxy import *
from voyager_system.tests.test_objects.DummyDatabase import DummyDatabase
from voyager_system.domain.medical_center.Consumer import Consumer
from voyager_system.domain.medical_center.Dosing import Dosing
from voyager_system.domain.medical_center.MedicalCenter import MedicalCenter
from voyager_system.domain.medical_center.Pod import *


class TestMarketplace(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMarketplace, self).__init__(*args, **kwargs)
        self.test_db = DummyDatabase(consumer_factory=consumer_factory)
        medical_center = MedicalCenter(db_proxy=DatabaseProxy())
        medical_center.db = self.test_db
        self.medical_center = medical_center

    def setUp(self):
        print('\nset up integration test')
        self.test_db.consumer_factory = consumer_factory
        pass

    def tearDown(self):
        print('tear down integration test')
        pass

    def test_get_consumer_success(self):
        print(f'Test: get consumer - success')
        consumer_id = 1
        consumer = self.medical_center.get_consumer(consumer_id)
        self.assertTrue(consumer)
        real_consumer = consumer_factory(consumer_id)

        self.assertEqual(consumer.id, real_consumer.id)
        self.assertEqual(consumer.first_name, real_consumer.first_name)
        self.assertEqual(consumer.last_name, real_consumer.last_name)
        self.assertEqual(consumer.residence, real_consumer.residence)


    def test_get_consumer_fail_1(self):
        print(f'Test: get consumer - fail 1')
        print(f'\tno consumer with the given id in the system')
        self.test_db.consumer_factory = consumer_factory_bad

        with self.assertRaises(AppOperationError):
            self.medical_center.get_consumer(1)
        pass

    def test_get_consumer_fail_2(self):
        print(f'Test: get consumer - fail 2')
        print(f'\tno connection with DB')
        self.test_db.consumer_factory = consumer_factory_broken

        with self.assertRaises(DataAccessError):
            self.medical_center.get_consumer(1)

    def test_get_consumer_dosing_history(self):
        print(f'Test: get consumer dosing history')
        consumer_id = 1
        history_dicts = self.medical_center.get_consumer_dosing_history(consumer_id)
        self.assertTrue(history_dicts is not None)
        real_history = consumer_factory(consumer_id).get_dosage_history()
        for dose_dict, dosing in zip(history_dicts, real_history):
            self.assertEqual(dose_dict['dosing_id'], dosing.id)

    async def test_get_consumer_pods(self):
        print(f'Test: get consumer pods')
        consumer_id = 1
        pod_dicts = self.medical_center.get_consumer_pods(consumer_id)
        self.assertTrue(pod_dicts is not None)
        real_pods = consumer_factory(consumer_id).get_pods()
        for pod_dict, pod in zip(pod_dicts, real_pods):
            self.assertEqual(pod_dict['serial_number'], pod.serial_number)

    async def test_consumer_dose_success(self):
        print(f'Test: consumer dose - success')
        consumer_id = 1
        consumer1 = consumer_factory(consumer_id)
        self.test_db.consumer_factory = lambda x: consumer1
        pod_serial = 'p_3'
        amount = 42.5
        self.medical_center.consumer_dose(consumer_id=consumer_id, pod_serial_num=pod_serial, amount=amount, time=timezone.now(), latitude=-2.0, longitude=-2.0)

        real_pod = consumer1.get_pod_by_serial_number(pod_serial)
        self.assertEqual(real_pod.remainder, 100 - amount)
        real_dosing = consumer1.dosing_history[0]
        self.assertEqual(real_dosing.amount, amount)
        self.assertEqual(real_dosing.pod_serial_number, pod_serial)

    async def test_consumer_dose_fail_1(self):
        print(f'Test: consumer dose - fail 1')
        print(f'\tno pods to dose from')
        consumer_id = 1
        consumer1 = consumer_factory(consumer_id)
        self.test_db.consumer_factory = lambda x: consumer1
        consumer1.pods = []
        with self.assertRaises(AppOperationError):
            self.medical_center.consumer_dose(consumer_id=consumer_id, pod_serial_num='p_2', amount=42.5,
                                              time=timezone.now(), latitude=-2.0, longitude=-2.0)

    async def test_consumer_dose_fail_2(self):
        print(f'Test: consumer dose - fail 2')
        print(f'\tincorrect pod id')
        with self.assertRaises(AppOperationError):
            self.medical_center.consumer_dose(consumer_id=1, pod_serial_num='p_1000', amount=42.5,
                                              time=timezone.now(), latitude=-2.0, longitude=-2.0)

    async def test_consumer_dose_fail_3(self):
        print(f'Test: consumer dose - fail 3')
        print(f'\tdosing amount too large')
        with self.assertRaises(AppOperationError):
            self.medical_center.consumer_dose(consumer_id=1, pod_serial_num='p_1', amount=1000.5,
                                              time=timezone.now(), latitude=-2.0, longitude=-2.0)


# test objects data
account_details1 = {'email': "michael@dundermifflin.com", 'pwd': 'scottstotts', 'phone': "9999999", 'f_name': "michael",
                    'l_name': "scott", 'dob': "1962-01-01"}
consumer_details1 = {'residence': 'Scranton, PA', 'height': 175, 'weight': 70, 'units': 1, 'gender': 1,
                     'goal': 'is there?'}
company_details = {'name': "E-corp"}
pod_type_details = {"name": "corpDrops",
                    'capacity': 100, 'company': company_details['name']}


# helper methods and factories
def consumer_factory(consumer_id):
    consumer = Consumer()
    consumer.id = consumer_id
    consumer.first_name = account_details1['f_name']
    consumer.last_name = account_details1['l_name']
    consumer.residence = consumer_details1['residence']

    pod_type_1 = PodType(name=pod_type_details['name'], capacity=pod_type_details['capacity'], company=company_details['name'],
                         substance="secret", description="done")
    time = parse_string_to_timezone('2022-05-01 18:00')
    dosings = [
        Dosing(dosing_id=i, pod_serial_number=f'p_{i // 2}', amount=20.0, time=time, longitude=-1.0, latitude=-1.0)
        for i in range(10)]
    pods = [Pod.from_type(f'p_{i}', pod_type_1) for i in range(5)]
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
