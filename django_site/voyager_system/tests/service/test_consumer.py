from django.test import TestCase

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

    def tearDown(self):
        print('tear down acceptance test')
        pass

    def test_get_consumer(self):
        consumer = self.db_proxy.get_consumer(57)
        self.skipTest("not implemented")