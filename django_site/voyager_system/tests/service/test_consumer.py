from django.test import TestCase

from voyager_system.domain.medical_center.Dispenser import Dispenser
from voyager_system.domain.medical_center.Pod import PodType, Pod
from voyager_system.service import ServiceSetup
import voyager_system.common.Result as Res

"""
    testing the functionality of the entire Guest API 
"""


class TestConsumer(TestCase):
    guest_service = ServiceSetup.get_guest_service()
    consumer_service = ServiceSetup.get_consumer_service()
    db_proxy = guest_service.system_management.db_proxy
    account1 = {'email': "micheal@dundermifflin.com", 'phone': "9999999", 'f_name': "micheal",
                'l_name': "scott", 'dob': "1962-01-01"}
    consumer1 = {'residence': 'Scranton, PA', 'height': 175, 'weight': 70, 'units': 1, 'gender': 1,
                 'goal': 'is there?'}
    account2 = {'email': "jim@dundermifflin.com", 'phone': "8888888", 'f_name': "jim",
                'l_name': "halpert", 'dob': "1979-01-01"}
    consumer2 = {'residence': 'Scranton, PA / philly, PA', 'height': 191, 'weight': 80, 'units': 1, 'gender': 1,
                 'goal': 'pam'}
    pod_type = {"name":"corpDrops"}
    pod1 = {"serial_number":"1_1"}
    pod2 = {"serial_number":"1_2"}

    def setUp(self):
        print('\nset up acceptance test')
        self.guest_service.create_account(email=self.account1['email'], phone=self.account1['phone'],
                                          f_name=self.account1['f_name'],
                                          l_name=self.account1['l_name'], dob=self.account1['dob'])
        self.guest_service.create_account(email=self.account2['email'], phone=self.account2['phone'],
                                          f_name=self.account2['f_name'],
                                          l_name=self.account2['l_name'], dob=self.account2['dob'])
        account = self.db_proxy.get_account_by_email(self.account1['email'])
        self.account1['id'] = account.id
        self.consumer1['id'] = account.id
        c1 = self.consumer1
        self.guest_service.create_consumer_profile(c1['id'], c1['residence'], c1['height'], c1['weight'], c1['units'],
                                                   c1['gender'], c1['goal'])
        account = self.db_proxy.get_account_by_email(self.account2['email'])
        self.account2['id'] = account.id
        self.consumer2['id'] = account.id
        self.db_proxy.add_company("E-corp")
        pod_type = PodType(name=self.pod_type['name'], capacity=40, substance="secret", description="done")
        self.db_proxy.add_pod_type(pod_type)
        real_consumer1 = self.db_proxy.get_consumer(self.consumer1['id'])
        self.db_proxy.add_pod(Pod(self.pod1['serial_number'],pod_type),real_consumer1)
        self.db_proxy.add_pod(Pod(self.pod2['serial_number'],pod_type),real_consumer1)
    def tearDown(self):
        print('tear down acceptance test')
        pass

    def test_register_pod_to_consumer(self):
        c2 = self.consumer2
        self.guest_service.create_consumer_profile(c2['id'], c2['residence'], c2['height'], c2['weight'], c2['units'],
                                                   c2['gender'], c2['goal'])
        real_consumer2 = self.db_proxy.get_consumer(self.consumer2['id'])
        self.consumer_service.register_pod_to_consumer(real_consumer2.id, self.pod1['serial_number'],self.pod_type['name'])
        # check if pod is related to consumer
        self.skipTest("not implemented")



    def test_get_consumer_and_some_other_stuff(self):
        # c2 = self.consumer2
        # self.guest_service.create_consumer_profile(c2['id'], c2['residence'], c2['height'], c2['weight'], c2['units'],
        #                                            c2['gender'], c2['goal'])
        #
        # # consumer = self.db_proxy.get_consumer(57)
        # self.db_proxy.add_company("E-corp")
        # pod_type = PodType(name="corpDrops", capacity=40, substance="secret", description="done")
        # self.db_proxy.add_pod_type(pod_type)

        # pod1 = Pod("1_1",pod_type)
        # pod2 = Pod("1_2",pod_type)
        # self.db_proxy.add_pod(pod1,consumer2)
        # self.db_proxy.add_pod(pod2,consumer2)
        #
        # dispenser = Dispenser()
        # dispenser.serial_number = "111"
        # dispenser.version = "mk1"
        # self.db_proxy.add_dispenser(dispenser)
        # consumer1 = self.db_proxy.get_consumer(self.consumer1['id'])
        # self.db_proxy.update_dispenser(dispenser,consumer1)
        # consumer1.register_pod(pod1)
        # consumer1.register_pod(pod2)
        # self.db_proxy.update_pod(pod1, consumer1)
        # self.db_proxy.update_pod(pod2, consumer1)
        # flag = True
        # consumer2again = self.db_proxy.get_consumer(consumer2.id)
        # consumer1again = self.db_proxy.get_consumer(consumer1.id)
        self.skipTest("not implemented")

