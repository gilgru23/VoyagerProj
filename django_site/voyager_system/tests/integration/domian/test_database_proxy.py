import unittest

import os


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
