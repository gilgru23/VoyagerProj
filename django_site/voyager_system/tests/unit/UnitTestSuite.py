import unittest
from voyager_system.tests.unit.domain.medicalCenter.test_consumer_class import TestConsumer


def extend_suite(suite, test_case):
    tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
    suite.addTests(tests)


def test_suite():
    # build suite
    suite = unittest.TestSuite()
    # add test-cases (test classes)
    extend_suite(suite, TestConsumer)
    # run suite
    unittest.TextTestRunner().run(suite)


if __name__ == '__main__':
    test_suite()
