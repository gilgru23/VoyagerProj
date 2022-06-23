from random import randint

from locust import HttpUser, task, between
import time


class QuickstartUser(HttpUser):
    wait_time = between(1, 4)
    consumer_details = {'residence': 'Scranton, PA', 'height': 175, 'weight': 70, 'units': 1, 'gender': 1,
                        'goal': 'is there?'}
    pod_details = None

    @task
    def perform_dose(self):
        params = {"pod_serial_num": self.pod_details['serial_number'],
                  "amount": 0.005, "time": '2020-05-20 16:05:00'}
        self.client.post("consumers/dose",json=params)

    @task(2)
    def view_pods(self):
        self.client.get("consumers/get_pods_of_consumer")

    def on_start(self):
        disp_id = randint(9, 9999999999999)
        dispenser_details = {"serial_number": f'd_{disp_id}', "version": f'V{randint(1, 9)}.{randint(1, 9)}'}
        pod_id = randint(9, 9999999999999)
        pod_details = {"serial_number": f'p_{pod_id}', "type_name": 'CorpDrops'}
        self.pod_details = pod_details
        account_details = {'email': f'{disp_id}@somemail.com', 'pwd': 'scottstotts', 'phone': "9999999",
                           'f_name': "michael", 'l_name': "scott", 'dob': "1962-01-01"}

        response = self.client.post("consumers/add_dispenser",
                                    json={'new_serial_number': dispenser_details['serial_number'],
                                          'version': dispenser_details['version']})
        print(f'\t\t@@ response msg: {response.content.decode("utf-8")}')
        response = self.client.post("consumers/add_pod", json={'new_serial_number': pod_details['serial_number'],
                                                               'pod_type': pod_details['type_name']})
        print(f'\t\t@@ response msg: {response.content.decode("utf-8")}')
        response = self.client.post("accounts/register_user", json=account_details)
        print(f'\t\t@@ response msg: {response.content.decode("utf-8")}')
        response = self.client.post("accounts/login_user", json=account_details)
        print(f'\t\t@@ response msg: {response.content.decode("utf-8")}')
        response = self.client.post("accounts/create_consumer_profile", json=self.consumer_details)
        print(f'\t\t@@ response msg: {response.content.decode("utf-8")}')

        response = self.client.post("consumers/register_dispenser",
                                    json={"serial_num": dispenser_details['serial_number'],
                                          "version": dispenser_details['version']})
        print(f'\t\t@@ response msg: {response.content.decode("utf-8")}')
        response = self.client.post("consumers/register_pod",
                                    json={"serial_num": pod_details['serial_number'],
                                          "pod_type": pod_details['type_name']})
        print(f'\t\t@@ response msg: {response.content.decode("utf-8")}')
