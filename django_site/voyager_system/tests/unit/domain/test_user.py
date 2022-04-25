import unittest
from voyager_system.domain.User import User


class TestUser(unittest.IsolatedAsyncioTestCase):
    user1 = User()

    def setUp(self):
        print('\nset up unit test')
        pass

    def tearDown(self):
        print('tear down unit test')
        pass

    # Unit Test Symbol: 6.1
    async def test_login_success(self):
        self.skipTest("method 'login' not implemented")

    # Unit Test Symbol: 6.1
    async def test_login_fail(self):
        self.skipTest("method 'login' not implemented")



if __name__ == '__main__':
    unittest.main()