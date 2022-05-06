import os
import unittest

# from voyager_system.service import ServiceSetup

"""
    testing the functionality of the entire Guest API 
"""


class TestGuest(unittest.TestCase):
    # guest_service = ServiceSetup.get_guest_service()

    def setUp(self):
        print('\nset up acceptance test')

    def tearDown(self):
        print('tear down acceptance test')
        pass

    # Acceptance Test Symbol: ?.?
    def test_register_user_success(self):
        # self.guest_service.create_account(email="1@here.com",phone="999999",f_name="john",l_name="john",dob="1/1/2000")
        self.skipTest("method 'request_dosing_reminder' not implemented")



def run_server_command():
    os.system("python manage.py runserver")


def close_server_command():
    raise NotImplementedError("Should have implemented this")


if __name__ == '__main__':
    run_server_command()
    unittest.main()
