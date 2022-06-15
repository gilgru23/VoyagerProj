import unittest

from voyager_system.common.ErrorTypes import AppOperationError
from voyager_system.domain.medical_center.Consumer import Consumer
from voyager_system.domain.medical_center.Dosing import *
from voyager_system.domain.medical_center.Pod import *

"""
    Unit Test Symbol corresponds to the enumeration in the Application Design Document.
    For example, 'Unit Test Symbol: 1.2' in this file (test_can_dose_[success/fail]) refers to the description
    of 'Unit 1: Consumer, Test 2: can-dose' in document   
"""


# noinspection SpellCheckingInspection
class TestConsumer(unittest.IsolatedAsyncioTestCase):
    consumer1 = Consumer()

    def setUp(self):
        print('\nset up unit test')
        pod_type_1 = PodType(name="111", capacity=100, description="None")
        dosings = [Dosing(dosing_id=i, pod_serial_number=f'{i // 2}',
                          amount=20, time=None, latitude=None, longitude=None) for i in range(10)]
        pods = [Pod.from_type(serial_number=f"{i}", pod_type=pod_type_1) for i in range(5)]
        self.consumer1.dosing_history = dosings
        self.consumer1.pods = pods
        pass

    def tearDown(self):
        print('tear down unit test')
        self.consumer1.dosing_history = []
        self.consumer1.pods = []
        pass

    # Unit Test Symbol: 1.1
    async def test_request_dosing_reminder_success(self):
        self.skipTest("method 'request_dosing_reminder' not implemented")

    # Unit Test Symbol: 1.1
    async def test_request_dosing_reminder_fail(self):
        self.skipTest("method 'request_dosing_reminder' not implemented")

    # Unit Test Symbol: 1.2
    async def test_can_dose_success(self):
        print(f'Test: can dose - success')
        dose_ans = self.consumer1.can_dose(serial_number='1', amount=42.5)
        self.assertTrue(dose_ans)

    # Unit Test Symbol: 1.2
    async def test_can_dose_fail(self):
        print(f'Test: can dose - fail')
        print(f'\tdosing amount too large')
        dose_ans = self.consumer1.can_dose(serial_number='1', amount=1000)
        self.assertFalse(dose_ans)

    # Unit Test Symbol: 1.3
    async def test_dose_success(self):
        print(f'Test: dose - success')
        self.consumer1.dose(pod_serial_number='1', amount=42.5, time_str=None)
        # check a new dosing was added to history at the front of the list
        new_dosing: Dosing = self.consumer1.dosing_history[0]
        self.assertEqual(new_dosing.pod_serial_number, "1")
        self.assertEqual(new_dosing.amount, 42.5)
        # check the pod remainder changed according to the amount of substance dosed
        pod = self.consumer1.get_pod_by_serial_number("1")
        self.assertTrue(pod)
        self.assertEqual(pod.remainder, 100 - 42.5)

    # Unit Test Symbol: 1.3
    async def test_dose_fail_1(self):
        print(f'Test: dose - fail')
        print(f'\tno pods to dose from')
        self.consumer1.pods = []
        with self.assertRaises(AppOperationError):
            self.consumer1.dose(pod_serial_number='1', amount=42.5, time_str=None)

    # Unit Test Symbol: 1.3
    async def test_dose_fail_2(self):
        print(f'Test: dose - fail')
        print(f'\tincorrect pod id')
        with self.assertRaises(AppOperationError):
            self.consumer1.dose(pod_serial_number='1000', amount=42.5, time_str=None)

    # Unit Test Symbol: 1.3
    async def test_dose_fail_3(self):
        print(f'Test: dose - fail')
        print(f'\tdosing amount too large')
        with self.assertRaises(AppOperationError):
            self.consumer1.dose(pod_serial_number='1', amount=1000, time_str=None)

    # Unit Test Symbol: 1.4
    async def test_get_dosing_history(self):
        print(f'Test: get dosing history - success')
        dosing = self.consumer1.get_dosage_history()
        dosing_output = dosing
        for d_out, d_hist in zip(dosing_output, self.consumer1.dosing_history):
            self.assertEqual(d_out, d_hist)

    # Unit Test Symbol: 1.5
    async def test_request_feedback_reminder_success(self):
        self.skipTest("method 'request_feedback_reminder' not implemented")

    # Unit Test Symbol: 1.5
    async def test_request_feedback_reminder_fail(self):
        self.skipTest("method 'request_feedback_reminder' not implemented")

    # Unit Test Symbol: 1.6
    async def test_provide_feedback_to_dose_success(self):
        print(f'Test: add feedback to dose - success')
        rating = 10
        d_id = 1
        comment = "it was very nice"
        self.consumer1.provide_feedback(dosing_id=d_id, feedback_rating=rating, feedback_comment=comment)
        past_dosings = [dose for dose in self.consumer1.dosing_history if dose.id == d_id]
        self.assertTrue(past_dosings, "no dosing after provide_feedback method call")
        feedback = past_dosings[0].feedback
        self.assertTrue(feedback, "no feedback after provide_feedback method call")
        self.assertTrue(feedback.comment == comment, "feedback doesnt match test input args")
        self.assertTrue(feedback.rating == rating, "feedback doesnt match test input args")

    # Unit Test Symbol: 1.6
    async def test_provide_feedback_to_dose_fail_1(self):
        print(f'Test: add feedback to dose - fail:')
        print(f'\t wrong dosing id')
        comment = "it was very nice"
        rating = 10
        d_id = 100
        with self.assertRaises(AppOperationError):
            self.consumer1.provide_feedback(dosing_id=d_id, feedback_rating=rating,
                                            feedback_comment=comment)

    # Unit Test Symbol: 1.6
    async def test_provide_feedback_to_dose_fail_2(self):
        print(f'Test: add feedback to dose - fail:')
        print(f'\t no dosing history records')
        self.consumer1.dosing_history = []
        comment = "it was very nice"
        rating = 10
        d_id = 1
        with self.assertRaises(AppOperationError):
            self.consumer1.provide_feedback(dosing_id=d_id, feedback_rating=rating,
                                            feedback_comment=comment)


if __name__ == '__main__':
    unittest.main()
