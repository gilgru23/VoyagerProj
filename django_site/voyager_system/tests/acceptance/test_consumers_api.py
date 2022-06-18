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

    account_details1 = {'email': "michael@dundermifflin.com", 'pwd': 'scottstotts', 'phone': "9999999", 'f_name': "michael",
                'l_name': "scott", 'dob': "1962-01-01"}
    consumer_details1 = {'residence': 'Scranton, PA', 'height': 175, 'weight': 70, 'units': 1, 'gender': 1,
                 'goal': 'is there?'}
    account_details2 = {'email': "jim@dundermifflin.com", 'pwd': '32edefdwQ', 'phone': "8888888", 'f_name': "jim",
                'l_name': "halpert", 'dob': "1979-01-01"}
    consumer_details2 = {'residence': 'Scranton, PA / philly, PA', 'height': 191, 'weight': 80, 'units': 1, 'gender': 1,
                 'goal': 'pam'}

    company_details = {'name': "E-corp"}

    dispenser_details1 = {'serial_number': "1515", 'version': "1.5"}
    dispenser_details2 = {'serial_number': "1212", 'version': "2.5"}

    pod_type_details = {"name": "corpDrops",
                        'capacity': 40, 'company': company_details['name']}

    pod_details1 = {"serial_number": "1_1",
                    "type_name": pod_type_details["name"]}
    pod_details2 = {"serial_number": "1_2",
                    "type_name": pod_type_details["name"]}
    pod_details3 = {"serial_number": "1_3",
                    "type_name": pod_type_details["name"]}
    pod_details4 = {"serial_number": "1_4",
                    "type_name": pod_type_details["name"]}

    def setUp(self):
        # Create 13 authors for pagination tests
        print('\nset up consumer acceptance test')
        self.setup_accounts()
        self.setup_pods()
        self.setup_dispensers()

    def setup_accounts(self):
        # register account 1
        body = json.dumps(self.account_details1)
        response = self.client1.generic('POST', reverse('register'), body)
        self.assertEqual(response.status_code, 200)
        # login account 1
        body = json.dumps(self.account_details1)
        response = self.client1.generic('POST', reverse('login'), body)
        self.assertEqual(response.status_code, 200)
        # create consumer 1 profile
        body = json.dumps(self.consumer_details1)
        response = self.client1.generic('GET', reverse('create consumer profile'), body)

        self.assertEqual(response.status_code, 200)
        # register account 2
        body = json.dumps(self.account_details2)
        response = self.client2.generic('POST', reverse('register'), body)
        self.assertEqual(response.status_code, 200)
        # login account 2
        body = json.dumps({'email': self.account_details2['email'], 'pwd': self.account_details2['pwd']})
        response = self.client2.generic('GET', reverse('login'), body)
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

    def register_dispenser_to_consumer(self, dispenser_details):
        params = {"serial_num": dispenser_details['serial_number'],
                  "version": dispenser_details['version']}
        body = json.dumps(params)
        response = self.client1.generic(
            'POST', reverse('register dispenser'), body)
        return response

    def register_pod_to_consumer(self, pod_details):
        params = {"serial_num": pod_details['serial_number'],
                  "pod_type": pod_details['type_name']}
        body = json.dumps(params)
        response = self.client1.generic('POST', reverse('register_pod'), body)
        return response

    def consumer_dose(self, pod_details, amount: float, time: str):
        params = {"pod_serial_num": pod_details['serial_number'],
                  "amount": amount, "time": time}
        body = json.dumps(params)
        response = self.client1.generic('POST', reverse('dose'), body)
        return response

    def get_dosing_history(self):
        response = self.client1.generic(
            'GET', reverse('get_dosing_history'), '')
        return response

    def add_feedback(self, dosing_id, feedback_rating: int, feedback_comment: str):
        params = {"dosing_id": dosing_id,
                  "rating": feedback_rating, "comment": feedback_comment}
        body = json.dumps(params)
        response = self.client1.generic(
            'POST', reverse('provide_feedback'), body)
        return response

    def get_feedback(self, dosing_id):
        params = {"dosing_id": dosing_id}
        response = self.client1.get(reverse('get_feedback_for_dosing'), params)

        return response

    def test_create_consumer_profile_success(self):
        print(f'\tTest: create consumer profile - success')
        body = json.dumps(self.consumer_details2)
        response = self.client2.generic('GET', reverse('create consumer profile'), body)
        self.assertEqual(response.status_code, 200)


    def test_create_consumer_profile_fail_1(self):
        print(f'\tTest: create consumer profile - fail')
        print(f'\t\tnot logged in to account')
        # check that a user that never registered cannot create a profile
        other_client = Client()
        body = json.dumps(self.consumer_details1)
        response = other_client.generic('GET', reverse('create consumer profile'), body)
        self.assertNotEqual(response.status_code, 200)
        # client 2 is logged in to account 2.
        # log out from account 2
        response = self.client2.generic('GET', reverse('logout'), "")
        self.assertEqual(response.status_code, 200)
        # check that a user that has logged out cannot create a profile
        response = self.client2.generic('GET', reverse('create consumer profile'), body)
        self.assertNotEqual(response.status_code, 200)


    def test_create_consumer_profile_fail_2(self):
        print(f'\tTest: create consumer profile - fail')
        print(f'\t\tconsumer profile already exists')
        body = json.dumps(self.consumer_details1)
        response = self.client1.generic('GET', reverse('create consumer profile'), body)
        self.assertEqual(response.status_code, 400)

    def test_register_dispenser_success(self):
        print(f'\tTest: register dispenser - success')
        # register dispenser1 to consumer
        response = self.register_dispenser_to_consumer(self.dispenser_details1)
        self.assertEqual(response.status_code, 200)

        # register dispenser2 to consumer
        response = self.register_dispenser_to_consumer(self.dispenser_details2)
        self.assertEqual(response.status_code, 200)

        # get consumer's dispensers
        response = self.client1.generic(
            'GET', reverse('get_dispensers_of_consumer'), '')
        self.assertEqual(response.status_code, 200)
        dispensers = json.loads(response.content)
        self.assertEqual(len(dispensers), 2)

    def test_register_dispenser_fail_1(self):
        print(f'\tTest: register dispenser - fail')
        print(f"\t\tthe dispenser's serial-number does not exist")
        # register dispenser1 to consumer
        response = self.register_dispenser_to_consumer({'serial_number':"notaRealSerialNumber", 'version':'None'})
        self.assertNotEqual(response.status_code, 200)

    def test_register_dispenser_fail_2(self):
        print(f'\tTest: register dispenser - fail')
        print(f"\t\tconsumer is not logged in")
        response = self.client1.generic('GET', reverse('logout'), "")
        self.assertEqual(response.status_code, 200)
        response = self.register_dispenser_to_consumer(self.dispenser_details1)
        self.assertNotEqual(response.status_code, 200)

    def test_register_dispenser_multiple_consumers_fail(self):
        print(f'\tTest: register dispenser multiple consumers - fail')
        # create consumer 2 profile
        body = json.dumps(self.consumer_details2)
        response = self.client2.generic('GET', reverse('create consumer profile'), body)
        # register dispenser1 to consumer
        response = self.register_dispenser_to_consumer(self.dispenser_details1)
        self.assertEqual(response.status_code, 200)

        # register dispenser2 to consumer
        params = {"serial_num": self.dispenser_details1['serial_number'],
                  "version": self.dispenser_details1['version']}
        body = json.dumps(params)
        response = self.client2.generic(
            'POST', reverse('register dispenser'), body)
        self.assertNotEqual(response.status_code, 200)
        print(f'\t\terror msg: {response.content.decode("utf-8")}')

    def test_consumer_dose_success(self, prt = True):
        if prt:
            print(f'\tTest: consumer dose - success')
        # register dispenser1 to consumer
        response = self.register_dispenser_to_consumer(self.dispenser_details1)
        self.assertEqual(response.status_code, 200)

        # register pods 1&2 to consumer
        response = self.register_pod_to_consumer(self.pod_details1)
        self.assertEqual(response.status_code, 200)
        response = self.register_pod_to_consumer(self.pod_details2)
        self.assertEqual(response.status_code, 200)

        # perform dosings
        response = self.consumer_dose(
            self.pod_details1, amount=1.5, time='2020-05-20 16:05:00')
        self.assertEqual(response.status_code, 200)
        response = self.consumer_dose(
            self.pod_details1, amount=1.0, time='2020-05-20 16:10:00')
        self.assertEqual(response.status_code, 200)
        response = self.consumer_dose(
            self.pod_details2, amount=0.5, time='2020-05-20 16:15:00')
        self.assertEqual(response.status_code, 200)

    def test_consumer_dose_fail_1(self):
        print(f'\tTest: consumer dose - fail')
        print(f'\t\t no dispenser is registered to consumer')

        # register pod 1 to consumer
        response = self.register_pod_to_consumer(self.pod_details1)
        self.assertEqual(response.status_code, 200)

        # perform dosings
        response = self.consumer_dose(
            self.pod_details1, amount=1.5, time='2020-05-20 16:05:00')
        self.assertNotEqual(response.status_code, 200)
        print(f'\t\terror msg: {response.content.decode("utf-8")}')

    def test_consumer_dose_fail_2(self):
        print(f'\tTest: consumer dose - fail')
        print(f'\t\tno pod is registered to consumer')
        # register dispenser1 to consumer
        response = self.register_dispenser_to_consumer(self.dispenser_details1)
        self.assertEqual(response.status_code, 200)

        # perform dosings
        response = self.consumer_dose(
            self.pod_details1, amount=1.5, time='2020-05-20 16:05:00')
        self.assertNotEqual(response.status_code, 200)
        print(f'\t\terror msg: {response.content.decode("utf-8")}')

    def test_consumer_dose_fail_3(self):
        print(f'\tTest: consumer dose - fail')
        print(f'\t\tsampled pod is empty')
        # register dispenser1 to consumer
        response = self.register_dispenser_to_consumer(self.dispenser_details1)
        self.assertEqual(response.status_code, 200)

        # register pod 1 to consumer
        response = self.register_pod_to_consumer(self.pod_details1)
        self.assertEqual(response.status_code, 200)

        # perform dosings
        response = self.consumer_dose(
            self.pod_details1, amount=40, time='2020-05-20 16:05:00')
        self.assertEqual(response.status_code, 200)
        response = self.consumer_dose(
            self.pod_details1, amount=0.5, time='2020-05-20 16:05:00')
        self.assertNotEqual(response.status_code, 200)
        print(f'\t\terror msg: {response.content.decode("utf-8")}')

    def test_get_dosing_history(self):
        print(f'\tTest: get dosing history - success')
        # perform dosings
        self.test_consumer_dose_success(prt=False)
        # get history
        response = self.get_dosing_history()
        self.assertEqual(response.status_code, 200)
        dosings = json.loads(response.content)
        self.assertEqual(len(dosings), 3)

    def test_register_pod(self):
        print(f'\tTest: register pod - success')
        response = self.register_pod_to_consumer(self.pod_details1)
        self.assertEqual(response.status_code, 200)

    def test_add_feedback_to_dosing(self):
        print(f'\tTest: add feedback to dosing - success')
        # perform dosing
        self.test_consumer_dose()
        # get history
        response = self.get_dosing_history()
        dosings = json.loads(response.content)
        # add feedback
        dosing_id = dosings[0]['dosing_id']
        response = self.add_feedback(dosing_id=dosing_id, feedback_rating=8,
                                     feedback_comment="it was good")
        self.assertEqual(response.status_code, 200)
        response = self.get_feedback(dosing_id=dosing_id)
        self.assertEqual(response.status_code, 200)
        feedback = json.loads(response.content)
        self.assertEqual(feedback['rating'], 8)
        self.assertEqual(feedback['comment'], "it was good")

    def test_get_feedback_fail(self):
        print(f'\tTest: get feedback - fail')
        print(f'\t\tno feedback was provided for the requested dosing')
        dosing_id = 1
        response = self.get_feedback(dosing_id=dosing_id)
        self.assertEqual(response.status_code, 400)
