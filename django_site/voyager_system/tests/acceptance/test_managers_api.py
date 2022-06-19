from django.test import TestCase, Client
from django.urls import reverse
import json

from voyager_system.domain.medical_center.Pod import *
from voyager_system.service import ServiceSetup


class TestManagers(TestCase):
    guest_service = ServiceSetup.get_guest_service()
    db_proxy = guest_service.system_management.db_proxy

    company_details = {'name': "E-corp"}
    pod_type_details = {"name": "corpDrops", 'capacity': 40, 'company': company_details['name']}

    def setUp(self):
        # Create 13 authors for pagination tests
        print('\nset up guest acceptance test')
        self.setup_pod_types()

    def setup_pod_types(self):
        self.db_proxy.add_company(self.company_details['name'])
        pod_type = PodType(name=self.pod_type_details['name'], capacity=40, company=self.company_details['name'],
                           substance="secret", description="done")
        self.db_proxy.add_pod_type(pod_type)

    def add_dispenser(self, serial_num, version):
        params = {"new_serial_num": serial_num, "version": version}
        body = json.dumps(params)
        response = self.client.generic('POST', reverse('add_dispenser'), body)
        return response

    def add_pod(self, serial_num, type_name):
        params = {"new_serial_num": serial_num, "pod_type": type_name}
        body = json.dumps(params)
        response = self.client.generic('POST', reverse('add_pod'), body)
        return response

    def test_add_dispenser(self):
        response = self.add_dispenser('d_1111', 'V3.1.2')
        self.assertEqual(response.status_code, 200)
        response = self.add_dispenser('d_1112', 'V3.1.2')
        self.assertEqual(response.status_code, 200)
        response = self.add_dispenser('d_1111', 'V3.1.2')
        self.assertNotEqual(response.status_code, 200)

    def test_add_pod(self):
        response = self.add_dispenser('d_1111', self.pod_type_details['name'])
        self.assertEqual(response.status_code, 200)
