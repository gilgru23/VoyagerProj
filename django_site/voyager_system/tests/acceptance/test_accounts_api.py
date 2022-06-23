from django.test import TestCase, Client
from django.urls import reverse
import json

from voyager_system.service import ServiceSetup


class TestAccounts(TestCase):

    guest_service = ServiceSetup.get_guest_service()
    db_proxy = guest_service.system_management.db_proxy

    account1 = {'email': "michael@dundermifflin.com", 'pwd': 'scottstotts', 'phone': "9999999", 'f_name': "michael",
                'l_name': "scott", 'dob': "1962-01-01"}
    consumer1 = {'residence': 'Scranton, PA', 'height': 175, 'weight': 70, 'units': 1, 'gender': 1,
                 'goal': 'is there?'}
    account2 = {'email': "jim@dundermifflin.com", 'pwd': '32edefdwQ', 'phone': "8888888", 'f_name': "jim",
                'l_name': "halpert", 'dob': "1979-01-01"}
    consumer2 = {'residence': 'Scranton, PA / philly, PA', 'height': 191, 'weight': 80, 'units': 1, 'gender': 1,
                 'goal': 'pam'}

    def setUp(self):
        # Create 13 authors for pagination tests
        print('\nset up guest acceptance test')
        # register account 1
        body = json.dumps(self.account1)
        response = self.client.generic('POST', reverse('register'), body)
        self.assertEqual(response.status_code, 200)
        # login account 1
        body = json.dumps(self.account1)
        response = self.client.generic('POST', reverse('login'), body)
        self.assertEqual(response.status_code, 200)
        # register account 2
        body = json.dumps(self.account2)
        response = self.client.generic('POST', reverse('register'), body)
        self.assertEqual(response.status_code, 200)


    def test_register_account_success(self):
        print(f'\tTest: register account - success')
        account = {"email": "sharon@there.com", "pwd": "AaSsDd12341234",
                   "phone": "0540545405", "f_name": "sharon", "l_name": "sharon",
                   "dob": "1990-05-05"}
        body = json.dumps(account)
        response = self.client.generic('POST', reverse('register'), body)
        self.assertEqual(response.status_code, 200)

    def test_register_account_fail_1(self):
        print(f'\tTest: register account - fail')
        print(f'\t\temail already taken')
        account = self.account1
        body = json.dumps(account)
        response = self.client.generic('POST', reverse('register'), body)
        self.assertNotEqual(response.status_code, 200)

    def test_register_account_fail_2(self):
        print(f'\tTest: register account - fail')
        print(f'\t\tinvalid password')
        account = {"email": "sharon@there.com", "pwd": "1234",
                   "phone": "0540545405", "f_name": "sharon", "l_name": "sharon",
                   "dob": "1990-05-05"}
        body = json.dumps(account)
        response = self.client.generic('POST', reverse('register'), body)
        self.assertNotEqual(response.status_code, 200)

    def test_login_to_account_success(self):
        print(f'\tTest: login to account - success')
        body = json.dumps({'email': self.account2['email'], 'pwd': self.account2['pwd']})
        response = self.client.generic('get', reverse('login'), body)
        self.assertEqual(response.status_code, 200)

    def test_login_to_account_fail_1(self):
        print(f'\tTest: login to account - fail')
        print(f'\t\temail is not registered')
        account = {'email':'notarealemail@nowhere.no', 'pwd':'324hR32fi@s'}
        body = json.dumps({'email': account['email'], 'pwd': account['pwd']})
        response = self.client.generic('get', reverse('login'), body)
        self.assertNotEqual(response.status_code, 200)

    def test_login_to_account_fail_2(self):
        print(f'\tTest: login to account - fail')
        print(f'\t\tincorrect password')
        account = {'email':self.account2['email'], 'pwd':'wrong_password'}
        body = json.dumps({'email': account['email'], 'pwd': account['pwd']})
        response = self.client.generic('get', reverse('login'), body)
        self.assertNotEqual(response.status_code, 200)

    def test_logout_from_account_success(self):
        print(f'\tTest: logout from account - success')
        body = ""
        response = self.client.generic('get', reverse('logout'), body)
        self.assertEqual(response.status_code, 200)

    def test_logout_from_account_fail(self):
        print(f'\tTest: logout from account - fail')
        print(f'\t\tclient is not logged-in')
        other_client = Client()
        body = ""
        response = other_client.generic('get', reverse('logout'), body)
        self.assertNotEqual(response.status_code, 200)


    def test_complex_scenario_1(self):
        """
        account 2 logs-in, creates a consumer profile and logs out.
        """
        # Login
        body = json.dumps({'email': self.account2['email'], 'pwd': self.account2['pwd']})
        response = self.client.generic('get', reverse('login'), body)
        self.assertEqual(response.status_code, 200)
        # Create consumer profile
        body = json.dumps(self.consumer2)
        response = self.client.generic('get', reverse('create consumer profile'), body)
        self.assertEqual(response.status_code, 200)
        # Logout
        body = ""
        response = self.client.generic('get', reverse('logout'), body)
        self.assertEqual(response.status_code, 200)



