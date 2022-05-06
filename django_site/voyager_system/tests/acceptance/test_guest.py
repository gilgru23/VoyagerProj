from django.test import TestCase

from voyager_system.service import ServiceSetup
import voyager_system.domain.common.Result as Res

"""
    testing the functionality of the entire Guest API 
"""


class TestGuest(TestCase):
    guest_service = ServiceSetup.get_guest_service()

    def setUp(self):
        print('\nset up acceptance test')

    def tearDown(self):
        print('tear down acceptance test')
        pass

    # Acceptance Test Symbol: ?.?
    def test_register_user_success(self):
        print(f'Test: register user - success:')
        result = self.guest_service.create_account(email="name@place.com", phone="999999", f_name="john",
                                                   l_name="john", dob="2000-01-01")
        self.assertTrue(Res.is_successful(result))

    # Acceptance Test Symbol: ?.?
    def test_register_user_fail(self):
        print(f'Test: register user - fail:')
        print(f'\t illegal email format')
        result = self.guest_service.create_account(email="1@here.com", phone="999999", f_name="john", l_name="john",
                                                   dob="2000-01-01")
        self.assertTrue(Res.is_failure(result))

