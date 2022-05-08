import unittest

import os

from voyager_system.dal.Util import DataAccessError
from voyager_system.domain.common.Util import AppOperationError
from voyager_system.tests.test_objects.DummyMapper import DummyMapper
from voyager_system.domain.DatabaseProxy import *
from voyager_system.tests.test_objects.DummyDatabase import DummyDatabase
from voyager_system.domain.medicalCenter.Consumer import Consumer
from voyager_system.domain.medicalCenter.Dosing import Dosing
from voyager_system.domain.medicalCenter.MedicalCenter import MedicalCenter
from voyager_system.domain.medicalCenter.Pod import *


class TestDatabaseProxy(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        super(TestDatabaseProxy, self).__init__(*args, **kwargs)
        pass

    def setUp(self):
        print('\nset up integration test')
        pass

    def tearDown(self):
        print('tear down integration test')
        pass

    async def test_db_example(self):
        print(f'Test: db example ')
        self.skipTest("not implemented")


def run_server_command():
    os.system("python manage.py runserver")

def close_server_command():
    raise NotImplementedError("Should have implemented this")



if __name__ == '__main__':
    # run_server_command()
    unittest.main()
    # close_server_command()
