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

    def test_add_dispenser(self):
        pass



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

    pod_type_1 = PodType(name=pod_type_details['name'], capacity=pod_type_details['capacity'],
                         company=company_details['name'],
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
