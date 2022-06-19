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


class TestConsumer(TransactionTestCase):
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

    def test_concurrent_pod_update(self):
        c_id1 = self.consumer_details1['id']
        p_d1 = self.pod_details1
        p_t_d = self.pod_type_details
        db = self.db_proxy

        # first 'task' gets pod
        pod1 = db.get_pod(p_d1['serial_number'])
        # first 'task' modifies pod
        pod1.remainder -= 1.5

        # second 'task' gets pod
        pod2 = db.get_pod(p_d1['serial_number'])
        # second 'task' modifies pod
        pod2.remainder -= 5
        # second 'task' saves modified pod
        db.update_pod(pod2, c_id1)

        with self.assertRaises(ConcurrentUpdateError):
            # first 'task' tries to override modifications,
            # throws concurrency error
            db.update_pod(pod1, c_id1)

        # first 'task' gets current version of pod
        pod1 = db.get_pod(p_d1['serial_number'])
        # first 'task' modifies current version of pod
        pod1.remainder -= 1.5
        # first 'task' saves modified pod
        db.update_pod(pod1, c_id1)
        print(f'updates are done')
        pods = db.get_consumer_pods(c_id1)
        # make sure pod was registered to consumer
        self.assertTrue(len(pods) == 1)
        # (value of len(pods) cannot be 2 because both 'tasks' modify the same pod)

        pod3 = pods[0]
        self.assertEqual(pod3.serial_number, p_d1['serial_number'])
        self.assertEqual(pod3.remainder, p_t_d['capacity'] - 5 - 1.5)
        self.assertEqual(pod3.obj_version, 2)

    def test_concurrent_pod_register(self):
        def register_pod_test():
            def task1(i):
                result = self.consumer_service.register_pod_to_consumer(c_id1, p_d1['serial_number'], p_d1['type_name'])
                # print(f'\t\ttask:{i}, result: {result[0]}, msg: {result[1]}\n')
                return result
            c_id1 = self.consumer_details1['id']
            p_d1 = self.pod_details1
            vals = [i for i in range(5)]
            results = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = executor.map(task1, vals)

            self.assertTrue(any([Res.is_failure(r) for r in results]))

        for i in range(10):
            register_pod_test()

    def test_concurrent_dose(self):
        def dose_test(j):
            def task1(i):
                result = self.consumer_service.consumer_dose(consumer_id=c_id1, pod_serial_num=p_d1['serial_number'],
                                                             amount=0.25, time=timezone.now(), longitude=42.76,
                                                             latitude=36.43)
                # print(f'\t\ttask:{i}, result: {result[0]}, msg: {result[1]}\n')
                return result

            reps = 4
            vals = [i for i in range(reps)]
            results = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = executor.map(task1, vals)

            self.assertTrue(all([Res.is_successful(r) for r in results]))
            pod = db.get_pod(p_d1['serial_number'])
            print(f'\tpod final state: serial number: {pod.serial_number} remainder: {pod.remainder}')
            self.assertEqual(pod.remainder, self.pod_type_details['capacity'] - (0.25 * reps * j))

        # setup consumer
        c_id1 = self.consumer_details1['id']
        p_d1 = self.pod_details1
        d_d1 = self.dispenser_details1
        db = self.db_proxy
        # register dispensers
        result = self.consumer_service.register_dispenser_to_consumer(c_id1, d_d1['serial_number'], d_d1['version'])
        self.assertTrue(Res.is_successful(result))
        result = self.consumer_service.register_pod_to_consumer(c_id1, p_d1['serial_number'], p_d1['type_name'])
        self.assertTrue(Res.is_successful(result))
        for i in range(6):
            dose_test(1+i)


    def test_concurrent_dose_different_pods(self):

        def get_pod_serial(n: int):
            return f'p_{n}'

        def dose_test(k):

            def task1(i):
                result = self.consumer_service.consumer_dose(consumer_id=c_id1, pod_serial_num=get_pod_serial(i),
                                                             amount=0.25, time=timezone.now(), longitude=42.76,
                                                             latitude=36.43)
                # print(f'\t\ttask:{i}, result: {result[0]}, msg: {result[1]}\n')
                return result

            vals = [j for j in range(sets)]
            results = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = executor.map(task1, vals)

            self.assertTrue(all([Res.is_successful(r) for r in results]))
            for j in range(sets):
                ser_num = get_pod_serial(j)
                pod = db.get_pod(ser_num)
                print(f'\t{j}: pod final state- serial number: {pod.serial_number} remainder: {pod.remainder}')
                self.assertEqual(pod.remainder, self.pod_type_details['capacity'] - 0.25 * k)


        # setup pods and register them to user
        pod_type = PodType(name=self.pod_type_details['name'], capacity=40, company=self.company_details['name'],
                           substance="secret", description="done")
        c_id1 = self.consumer_details1['id']
        p_d1 = {"serial_number": "1_1", 'type_name': self.pod_type_details['name']}
        d_d1 = self.dispenser_details1
        db = self.db_proxy
        sets = 8
        for i in range(sets):
            p_d1['serial_number'] = get_pod_serial(i)
            pod1 = Pod.from_type(p_d1['serial_number'], pod_type)
            db.add_pod(pod1)
            result = self.consumer_service.register_pod_to_consumer(c_id1, p_d1['serial_number'], p_d1['type_name'])
            self.assertTrue(Res.is_successful(result))

        # register dispensers
        result = self.consumer_service.register_dispenser_to_consumer(c_id1, d_d1['serial_number'], d_d1['version'])
        self.assertTrue(Res.is_successful(result))
        for i in range(sets):
            dose_test(1+i)
