import unittest

from voyager_system.tests.unit.domain.test_user import TestUser
from voyager_system.tests.unit.domain.medicalCenter.test_consumer import TestConsumer


# def extend_suite(suite, test_case):
#     tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
#     suite.addTests(tests)
#
#
# def test_suite():
#     # build suite
#     suite = unittest.TestSuite()
#     # add test-cases (test classes)
#     extend_suite(suite, TestConsumer)
#     extend_suite(suite, TestUser)
#     # run suite
#     unittest.TextTestRunner().run(suite)


if __name__ == '__main__':
    unittest.main()
