from django.test import TestCase, Client
from django.urls import reverse
import json

from voyager_system.domain.medical_center.Dispenser import Dispenser
from voyager_system.domain.medical_center.Pod import PodType, Pod
from voyager_system.service import ServiceSetup


class TestConsumers(TestCase):

    consumer_service = ServiceSetup.get_consumer_service()
    db_proxy = ServiceSetup.get_db_proxy()

    client1 = Client()
    client2 = Client()

    account1 = {'email': "micheal@dundermifflin.com", 'pwd': 'scottstotts', 'phone': "9999999", 'f_name': "micheal",
                'l_name': "scott", 'dob': "1962-01-01"}
    consumer1 = {'residence': 'Scranton, PA', 'height': 175, 'weight': 70, 'units': 1, 'gender': 1,
                 'goal': 'is there?'}
    account2 = {'email': "jim@dundermifflin.com", 'pwd': '32edefdwQ', 'phone': "8888888", 'f_name': "jim",
                'l_name': "halpert", 'dob': "1979-01-01"}
    consumer2 = {'residence': 'Scranton, PA / philly, PA', 'height': 191, 'weight': 80, 'units': 1, 'gender': 1,
                 'goal': 'pam'}
    company_details = {'name': "E-corp"}
    dispenser_details1 = {'serial_number': "1515", 'version': "1.5"}
    dispenser_details2 = {'serial_number': "1212", 'version': "2.5"}
    pod_type_details = {"name": "corpDrops", 'capacity': 40, 'company': company_details['name']}
    pod_details1 = {"serial_number": "1_1"}
    pod_details2 = {"serial_number": "1_2"}
    pod_details3 = {"serial_number": "1_3"}
    pod_details4 = {"serial_number": "1_4"}

    def setUp(self):
        # Create 13 authors for pagination tests
        print('\nset up guest acceptance test')
        self.setup_accounts()
        self.setup_pods()
        self.setup_dispensers()

    def setup_accounts(self):
        # register account 1
        body = json.dumps(self.account1)
        response = self.client1.generic('POST', reverse('register'), body)
        self.assertEqual(response.status_code, 200)
        # login account 1
        body = json.dumps(self.account1)
        response = self.client1.generic('POST', reverse('login'), body)
        self.assertEqual(response.status_code, 200)
        # create consumer 1 profile
        body = json.dumps(self.consumer1)
        response = self.client1.generic('get', reverse('create consumer profile'), body)
        self.assertEqual(response.status_code, 200)
        # register account 2
        body = json.dumps(self.account2)
        response = self.client2.generic('POST', reverse('register'), body)
        self.assertEqual(response.status_code, 200)
        # login account 2
        body = json.dumps({'email': self.account2['email'], 'pwd': self.account2['pwd']})
        response = self.client2.generic('get', reverse('login'), body)
        self.assertEqual(response.status_code, 200)

    def setup_pods(self):
        self.db_proxy.add_company(self.company_details['name'])
        pod_type = PodType(name=self.pod_type_details['name'], capacity=40, company=self.company_details['name'],
                           substance="secret", description="done")
        self.db_proxy.add_pod_type(pod_type)
        pod1 = Pod.from_type(self.pod_details1['serial_number'], pod_type)
        pod2 = Pod.from_type(self.pod_details2['serial_number'], pod_type)
        pod3 = Pod.from_type(self.pod_details3['serial_number'], pod_type)
        pod4 = Pod.from_type(self.pod_details4['serial_number'], pod_type)
        self.db_proxy.add_pod(pod1)
        self.db_proxy.add_pod(pod2)
        self.db_proxy.add_pod(pod3)
        self.db_proxy.add_pod(pod4)

    def setup_dispensers(self):
        disp = Dispenser()
        disp.serial_number = self.dispenser_details1['serial_number']
        disp.version = self.dispenser_details1['version']
        self.db_proxy.add_dispenser(disp)
        disp.serial_number = self.dispenser_details2['serial_number']
        disp.version = self.dispenser_details2['version']
        self.db_proxy.add_dispenser(disp)


    def test_register_pod(self):
        params = {"serial_num": self.pod_details1['serial_number'],
                  "pod_type": self.pod_type_details['name']}
        body = json.dumps(params)
        response = self.client1.generic('POST', reverse('register_pod'), body)
        self.assertEqual(response.status_code, 200)
