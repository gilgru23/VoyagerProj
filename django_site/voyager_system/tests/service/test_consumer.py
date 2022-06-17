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
        p_d1 = self.pod_details1
        p_d2 = self.pod_details2
        p_d3 = self.pod_details3
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

    def my_tests2(self):
        c_id1 = self.consumer_details1['id']
        p_d1 = self.pod_details1
        db = self.db_proxy

        # with transaction.atomic():
        #     pod, db_pod = db.get_pod2(p_d1['serial_number'])
        #     pod.remainder -= 1.5
        #     print(f'task1 going to sleep')
        #     time.sleep(4)
        #     print(f'task1 woke up')
        #     db.update_pod2(pod,db_pod,c_id1)

        # self.helper_get_pod_lock()

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     print('executor')
        #     future1 = executor.submit(self.helper_get_pod_lock)
        #     future1.add_done_callback(self.on_done)
        #     future2 = executor.submit(self.helper_get_pod_no_lock)
        #     future2.add_done_callback(self.on_done)
        #
        #     res1 = future1.result()
        #     res2 = future2.result()

        t1 = threading.Thread(target=self.helper_get_pod_lock, args=[])
        t2 = threading.Thread(target=self.helper_get_pod_no_lock, args=[], daemon=True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        print(f'Main task going to sleep')
        time.sleep(2)
        pods = db.get_consumer_pods(c_id1)
        for pod0 in pods:
            print(f'\tpod:{pod0.serial_number}, remainder:{pod0.remainder}')
        print(f'Main task Done!')

        # print("pods")
        pass

    def on_done(self, future):
        connections.close_all()

    def helper_get_pod_lock(self):
        print(f'task1 is starting')
        c_id1 = self.consumer_details1['id']
        p_d1 = self.pod_details1
        db = self.db_proxy

        with transaction.atomic():
            pod, db_pod = db.get_pod2(p_d1['serial_number'])
            print(f'task1 got pod, pod:{pod.serial_number}, remainder:{pod.remainder}')
            pod.remainder -= 1.5
            print(f'task1 going to sleep')
            time.sleep(5)
            print(f'task1 woke up')
            db.update_pod2(pod, db_pod, c_id1)
            print(f'task1 Done!')

        pass

    def helper_get_pod_no_lock(self):
        print(f'task2 is starting')
        print(f'task2 going to sleep')
        time.sleep(2)
        print(f'task2 woke up')
        c_id1 = self.consumer_details1['id']
        p_d1 = self.pod_details1
        db = self.db_proxy

        with transaction.atomic():
            pod0, sb_pod0 = db.get_pod2(p_d1['serial_number'])
            print(f'task2 Done! pod:{pod0.serial_number}, remainder:{pod0.remainder}')
        pass

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

    def test_concurrent_pod_update_2(self):
        for i in range(20):
            self.update_test_2()

    def update_test_2(self):
        def task1(i):
            # print(f'reg-pod #{i} starting')
            result = self.consumer_service.register_pod_to_consumer(c_id1, p_d1['serial_number'], p_d1['type_name'])
            # print(f'#{i} result: {Res.is_successful(result)}, msg: {result[1]}\n')
            return result

        c_id1 = self.consumer_details1['id']
        p_d1 = self.pod_details1
        db = self.db_proxy
        vals = [i for i in range(2)]
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # print('executor')
            results = executor.map(task1, vals)

        self.assertTrue(any([Res.is_failure(r) for r in results]))

    def test_tests(self):
        c_id1 = self.consumer_details1['id']
        p_d1 = self.pod_details1
        p_d2 = self.pod_details2
        result = self.consumer_service.register_pod_to_consumer(c_id1, p_d1['serial_number'], p_d1['type_name'])
        self.assertTrue(Res.is_successful(result))
        # result = self.consumer_service.register_pod_to_consumer(c_id1, p_d1['serial_number'], p_d1['type_name'])
        # self.assertTrue(Res.is_successful(result))
        # self.consumer_service.register_pod_to_consumer(c_id1, p_d2['serial_number'], p_d2['type_name'])
