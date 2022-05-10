from django.test import TestCase

from voyager_system.service import ServiceSetup
import voyager_system.common.Result as Res

"""
    testing the functionality of the entire Guest API 
"""


class TestGuest(TestCase):
    guest_service = ServiceSetup.get_guest_service()
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
        print('\nset up guest service test')
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
        print('tear down service test')
        pass

    def test_register_user_success(self):
        print(f'Test: register user - success:')
        result = self.guest_service.create_account(email="dwight@dundermifflin.com", phone="7777777", f_name="dwight",
                                                   l_name="schrute", dob="1966-01-01")
        self.assertTrue(Res.is_successful(result))

    def test_register_user_fail1(self):
        print(f'Test: register user - fail:')
        print(f'\t illegal email format')
        result = self.guest_service.create_account(email="1@here.com", phone="999999", f_name="john",
                                                   l_name="john", dob="2000-01-01")
        self.assertTrue(Res.is_failure(result))

    def test_register_user_fail2(self):
        print(f'Test: register user - fail:')
        print(f'\t account already exists')
        a1 = self.account1
        result = self.guest_service.create_account(email=a1['email'], phone=a1['phone'],
                                                   f_name=a1['f_name'], l_name=a1['l_name'], dob=a1['dob'])
        self.assertTrue(Res.is_failure(result))

    def test_create_consumer_profile_success(self):
        print(f'Test: create consumer profile - success:')
        c2 = self.consumer2
        result = self.guest_service.create_consumer_profile(c2['id'], c2['residence'], c2['height'], c2['weight'],
                                                            c2['units'], c2['gender'], c2['goal'])
        self.assertTrue(Res.is_successful(result))
        ans = self.guest_service.system_management.is_consumer(c2['id'])
        self.assertTrue(ans)

    def test_create_consumer_profile_fail1(self):
        print(f'Test: create consumer profile - fail:')
        print(f'\t account does not exist')
        result = self.guest_service.create_consumer_profile(3, "nowhere", 160, 60, 1, 1, None)
        self.assertTrue(Res.is_failure(result))

    def test_create_consumer_profile_fail2(self):
        print(f'Test: create consumer profile - fail:')
        print(f'\t account is already a consumer')
        c1 = self.consumer1
        result = self.guest_service.create_consumer_profile(c1['id'], c1['residence'], c1['height'], c1['weight'],
                                                            c1['units'], c1['gender'], c1['goal'])
        self.assertTrue(Res.is_failure(result))


