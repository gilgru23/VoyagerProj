
from django.test import TestCase

from voyager_system.domain.medical_center.Dispenser import Dispenser
from voyager_system.domain.medical_center.Dosing import Dosing
from voyager_system.domain.medical_center.Pod import PodType, Pod
from voyager_system.service import ServiceSetup


# noinspection SpellCheckingInspection
class TestConsumer(TestCase):
    # main units to be tested
    db = ServiceSetup.get_db_proxy()

    # objects details for setUp
    account_details1 = {'email': "micheal@dundermifflin.com", 'phone': "9999999", 'f_name': "micheal",
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
    pod_type_details = {"name": "corpDrops", 'capacity': 40, 'company': company_details['name']}
    pod_details1 = {"serial_number": "1_1"}
    pod_details2 = {"serial_number": "1_2"}
    pod_details3 = {"serial_number": "1_3"}
    pod_details4 = {"serial_number": "1_4"}

    def setUp(self):
        print('\nset up acceptance test')
        #  register two accounts
        self.db.add_account(email=self.account_details1['email'], phone=self.account_details1['phone'],
                                          first_name=self.account_details1['f_name'],
                                          last_name=self.account_details1['l_name'], date_of_birth=self.account_details1['dob'])
        self.db.add_account(email=self.account_details2['email'], phone=self.account_details2['phone'],
                                          first_name=self.account_details2['f_name'],
                                          last_name=self.account_details2['l_name'], date_of_birth=self.account_details2['dob'])
        # get account id back
        account = self.db.get_account_by_email(self.account_details1['email'])
        self.account_details1['id'] = account.id
        self.consumer_details1['id'] = account.id
        c1 = self.consumer_details1
        account = self.db.get_account_by_email(self.account_details2['email'])
        self.account_details2['id'] = account.id
        self.consumer_details2['id'] = account.id

        # register consumer for account 1
        self.db.add_consumer(c1['id'], c1['residence'], c1['height'], c1['weight'], c1['units'],
                                                   c1['gender'], c1['goal'])

        # register pods
        print(" ")
        self.db.add_company(self.company_details['name'])
        pod_type = PodType(name=self.pod_type_details['name'], capacity=40, company=self.company_details['name'],
                           substance="secret", description="done")
        self.db.add_pod_type(pod_type)
        pod1 = Pod.from_type(self.pod_details1['serial_number'], pod_type)
        pod2 = Pod.from_type(self.pod_details2['serial_number'], pod_type)
        pod3 = Pod.from_type(self.pod_details3['serial_number'], pod_type)
        pod4 = Pod.from_type(self.pod_details4['serial_number'], pod_type)
        self.db.add_pod(pod1)
        self.db.add_pod(pod2)
        self.db.add_pod(pod3)
        self.db.add_pod(pod4)
        disp = Dispenser()
        disp.serial_number = self.dispenser_details1['serial_number']
        disp.version = self.dispenser_details1['version']
        self.db.add_dispenser(disp)
        disp.serial_number = self.dispenser_details2['serial_number']
        disp.version = self.dispenser_details2['version']
        self.db.add_dispenser(disp)

    def tearDown(self) -> None:
        print('\ntear down acceptance test')

    def test_pods_add_update_get(self):
        print(f'Test: pods add update get')
        # get pods
        pod1 = self.db.get_pod(self.pod_details1['serial_number'])
        pod2 = self.db.get_pod(self.pod_details2['serial_number'])
        # register to a consumer
        self.db.update_pod(pod1, self.consumer_details1['id'])
        self.db.update_pod(pod2, self.consumer_details1['id'])
        # check if pods are related to consumer
        pods = self.db.get_consumer_pods(self.consumer_details1['id'])
        self.assertEqual(len(pods), 2)

    def test_dosings_add_update_get(self):
        print(f'Test: pods add update get')
        # add dosings
        dosing1 = Dosing()
        # get dosings
        pod1 = self.db.get_pod(self.pod_details1['serial_number'])
        pod2 = self.db.get_pod(self.pod_details2['serial_number'])
        # register to a consumer
        self.db.update_pod(pod1, self.consumer_details1['id'])
        self.db.update_pod(pod2, self.consumer_details1['id'])
        # check if pods are related to consumer
        pods = self.db.get_consumer_pods(self.consumer_details1['id'])
        self.assertEqual(len(pods), 2)