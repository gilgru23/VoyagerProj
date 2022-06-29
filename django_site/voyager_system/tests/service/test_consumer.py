from django.test import TestCase
from django.utils import timezone

from voyager_system.common.ErrorTypes import ConcurrentUpdateError
from voyager_system.domain.medical_center.Dispenser import Dispenser
from voyager_system.domain.medical_center.Pod import PodType, Pod
from voyager_system.service import ServiceSetup
import voyager_system.common.Result as Res

from django.db import transaction
import time
import threading
import concurrent.futures
from django.db import connections
from django.test import TransactionTestCase

"""
    testing the functionality of the entire Guest API 
"""


class TestConsumer(TestCase):
    # main units to be tested
    guest_service = ServiceSetup.get_guest_service()
    consumer_service = ServiceSetup.get_consumer_service()
    db_proxy = guest_service.system_management.db_proxy

    # objects details for setUp
    account_details1 = {'email': "michael@dundermifflin.com", 'phone': "9999999", 'f_name': "michael",
                        'l_name': "scott", 'dob': "1962-01-01"}
    consumer_details1 = {'residence': 'Scranton, PA', 'height': 175, 'weight': 70, 'units': 1, 'gender': 1,
                         'goal': 'is there?'}
    account_details2 = {'email': "jim@dundermifflin.com", 'phone': "8888888", 'f_name': "jim",
                        'l_name': "halpert", 'dob': "1979-01-01"}
    consumer_details2 = {'residence': 'Scranton, PA / philly, PA', 'height': 191, 'weight': 80, 'units': 1, 'gender': 1,
                         'goal': 'pam'}
    company_details = {'name': "E-corp"}
    dispenser_details1 = {'serial_number': "1515", 'version': "1.5"}
    dispenser_details2 = {'serial_number': "1212", 'version': "2.5"}
    pod_type_details = {"name": "corpDrops", 'capacity': 40.0, 'company': company_details['name']}
    pod_details1 = {"serial_number": "1_1", 'type_name': pod_type_details['name']}
    pod_details2 = {"serial_number": "1_2", 'type_name': pod_type_details['name']}
    pod_details3 = {"serial_number": "1_3", 'type_name': pod_type_details['name']}
    pod_details4 = {"serial_number": "1_4", 'type_name': pod_type_details['name']}

    def setUp(self):
        print('\nset up service test')
        #  register two accounts
        self.guest_service.create_account(email=self.account_details1['email'], phone=self.account_details1['phone'],
                                          f_name=self.account_details1['f_name'],
                                          l_name=self.account_details1['l_name'], dob=self.account_details1['dob'])
        self.guest_service.create_account(email=self.account_details2['email'], phone=self.account_details2['phone'],
                                          f_name=self.account_details2['f_name'],
                                          l_name=self.account_details2['l_name'], dob=self.account_details2['dob'])
        # get account id back
        account = self.db_proxy.get_account_by_email(self.account_details1['email'])
        self.account_details1['id'] = account.id
        self.consumer_details1['id'] = account.id
        c1 = self.consumer_details1
        account = self.db_proxy.get_account_by_email(self.account_details2['email'])
        self.account_details2['id'] = account.id
        self.consumer_details2['id'] = account.id

        # register consumer for account 1
        self.guest_service.create_consumer_profile(c1['id'], c1['residence'], c1['height'], c1['weight'], c1['units'],
                                                   c1['gender'], c1['goal'])
        # register pods
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
        disp = Dispenser()
        disp.serial_number = self.dispenser_details1['serial_number']
        disp.version = self.dispenser_details1['version']
        self.db_proxy.add_dispenser(disp)
        disp.serial_number = self.dispenser_details2['serial_number']
        disp.version = self.dispenser_details2['version']
        self.db_proxy.add_dispenser(disp)

    def tearDown(self) -> None:
        print('\ntear down service test')

    def test_register_pod_to_consumer(self):
        real_consumer1 = self.db_proxy.get_consumer(self.consumer_details1['id'])
        result = self.consumer_service.register_pod_to_consumer(real_consumer1.id, self.pod_details1['serial_number'],
                                                                self.pod_type_details['name'])
        self.assertTrue(Res.is_successful(result))
        result = self.consumer_service.register_pod_to_consumer(real_consumer1.id, self.pod_details2['serial_number'],
                                                                self.pod_type_details['name'])

        # check if pods are related to consumer
        pods = self.db_proxy.get_consumer_pods(real_consumer1.id)
        self.assertEqual(len(pods), 2)

    def test_get_consumer_pods(self):
        consumer1_id = self.consumer_details1['id']
        result = self.consumer_service.register_pod_to_consumer(consumer1_id, self.pod_details1['serial_number'],
                                                                self.pod_type_details['name'])
        self.assertTrue(Res.is_successful(result))
        result = self.consumer_service.register_pod_to_consumer(consumer1_id, self.pod_details2['serial_number'],
                                                                self.pod_type_details['name'])
        self.assertTrue(Res.is_successful(result))
        result = self.consumer_service.register_pod_to_consumer(consumer1_id, self.pod_details3['serial_number'],
                                                                self.pod_type_details['name'])
        self.assertTrue(Res.is_successful(result))
        # check if pods are related to consumer
        result = self.consumer_service.get_consumer_pods(consumer1_id)
        pod_dicts = Res.get_value(result)
        self.assertEqual(len(pod_dicts), 3)
        list(pod_dicts).sort(key=lambda x: x['serial_number'])
        pods_details = [self.pod_details1, self.pod_details2, self.pod_details3]
        pods_details.sort(key=lambda x: x['serial_number'])
        for pod_dict, pod_details in zip(pod_dicts, pods_details):
            self.assertEqual(pod_dict['serial_number'], pod_details['serial_number'])

    def test_register_dispenser_to_consumer(self):
        consumer1_id = self.consumer_details1['id']
        # register dispensers
        result = self.consumer_service.register_dispenser_to_consumer(consumer1_id,
                                                                      self.dispenser_details1['serial_number'],
                                                                      self.dispenser_details1['version'])
        self.assertTrue(Res.is_successful(result))
        result = self.consumer_service.register_dispenser_to_consumer(consumer1_id,
                                                                      self.dispenser_details2['serial_number'],
                                                                      self.dispenser_details2['version'])
        self.assertTrue(Res.is_successful(result))

        # check if pods are related to consumer
        dispensers = self.db_proxy.get_consumer_dispensers(consumer1_id)
        self.assertEqual(len(dispensers), 2)

    def test_consumer_dose(self):
        c_id1 = self.consumer_details1['id']
        d_d1 = self.dispenser_details1
        p_d1 = self.pod_details1
        p_d2 = self.pod_details2
        p_d3 = self.pod_details3
        self.consumer_service.register_dispenser_to_consumer(c_id1,d_d1['serial_number'],d_d1['version'])
        self.consumer_service.register_pod_to_consumer(c_id1, p_d1['serial_number'], p_d1['type_name'])
        self.consumer_service.register_pod_to_consumer(c_id1, p_d2['serial_number'], p_d2['type_name'])
        self.consumer_service.register_pod_to_consumer(c_id1, p_d3['serial_number'], p_d3['type_name'])

        result = self.consumer_service.consumer_dose(consumer_id=c_id1, pod_serial_num=p_d2['serial_number'],
                                                     amount=0.5, time=timezone.now(), longitude=42.76, latitude=36.43)
        self.assertTrue(Res.is_successful(result))
        result = self.consumer_service.consumer_dose(consumer_id=c_id1, pod_serial_num=p_d3['serial_number'],
                                                     amount=1.5, time=timezone.now(), longitude=42.76, latitude=36.43)
        self.assertTrue(Res.is_successful(result))

        result = self.consumer_service.get_consumer_dosing_history(c_id1)
        self.assertTrue(Res.is_successful(result))
        history = Res.get_value(result)
        self.assertEqual(len(history), 2)


    def test_caregiver_gets_consumer_history(self):
        print(f'Test: register caregiver to consumer - success:')
        a3 = {'email': "pam@dundermifflin.com", 'phone': "9999999", 'f_name': "pam",
              'l_name': "beasly", 'dob': "1980-01-01"}
        c3 = {'residence': 'Scranton, PA / philly, PA', 'height': 167, 'weight': 50, 'units': 1, 'gender': 2,
              'goal': 'jim'}

        self.guest_service.create_account(email=a3['email'], phone=a3['phone'],
                                          f_name=a3['f_name'],
                                          l_name=a3['l_name'], dob=a3['dob'])
        account = self.db_proxy.get_account_by_email(a3['email'])
        a3['id'] = account.id
        c3['id'] = account.id
        self.guest_service.create_consumer_profile(c3['id'], c3['residence'], c3['height'], c3['weight'], c3['units'],
                                                   c3['gender'], c3['goal'])
        a2 = self.account_details2
        c1 = self.consumer_details1

        result = self.guest_service.create_caregiver_profile(a2['id'])
        self.assertTrue(Res.is_successful(result))
        result = self.consumer_service.register_caregiver_to_consumer(consumer_id=c1['id'],
                                                                              caregiver_email=a2['email'])
        self.assertTrue(Res.is_successful(result))
        result = self.consumer_service.register_caregiver_to_consumer(consumer_id=c3['id'],
                                                                              caregiver_email=a2['email'])
        self.assertTrue(Res.is_successful(result))
        self.test_consumer_dose()
        result = self.consumer_service.get_consumer_history_for_caregiver(caregiver_id=a2['id'],consumer_id=c1['id'])
        self.assertTrue(Res.is_successful(result))
        history = Res.get_value(result)
        print(history)
