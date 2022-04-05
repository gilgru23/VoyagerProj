import unittest

from domain.medicalCenter.Consumer import Consumer
from domain.medicalCenter.Dosing import *
from domain.medicalCenter.Pod import *


class TestConsumer(unittest.TestCase):


    consumer1 = Consumer()
    consumer1.first_name = 'Gil'

    def setUp(self):
        print('set up unit test')
        dosings = [Dosing(dosing_id=i, pod_id=i//2, amount=20, time=None, location=None) for i in range(10)]
        pod_type_1 = PodType(type_id=111, capacity=100)
        pods = [Pod(pod_id=i,pod_type=pod_type_1) for i in range(5)]
        self.consumer1.dosing_history.extend(dosings)
        self.consumer1.pods.extend(pods)
        pass


    def tearDown(self):
        print('tear down unit test')
        self.consumer1.dosing_history = []
        self.consumer1.pods = []
        pass


    def test_0_get_dosing_history(self):
        print(f'Test: get dosing history')
        dosing_output = self.consumer1.get_dosage_history()
        for d_out,d_hist in zip(dosing_output, self.consumer1.dosing_history):
            self.assertEqual(d_out,d_hist)


    def test_1_dose_success(self):
        print(f'Test: dose - success')
        result = self.consumer1.dose(pod_id=1, amount=42.5,location='here')
        self.assertTrue(result)
        # check a new dosing was added to history at the front of the list
        new_dosing: Dosing = self.consumer1.dosing_history[0]
        self.assertEqual(new_dosing.pod_id, 1)
        self.assertEqual(new_dosing.amount, 42.5)
        # check the pod remainder changed according to the amount of substance dosed
        pod: Pod = self.consumer1.get_pod_by_id(1)
        self.assertEqual(pod.remainder, 100 - 42.5)


    def test_2_dose_fail1(self):
        print(f'Test: dose - fail')
        print(f'\nno pods to dose from')
        self.consumer1.pods = []
        result = self.consumer1.dose(pod_id=1, amount=42.5,location='here')
        self.assertFalse(result)

    def test_3_dose_fail2(self):
        print(f'Test: dose - fail')
        print(f'\nno incorrect pod id')
        result = self.consumer1.dose(pod_id=1000, amount=42.5,location='here')
        self.assertFalse(result)

    def test_4_dose_fail3(self):
        print(f'Test: dose - fail')
        print(f'\nno dosing amount too large')
        result = self.consumer1.dose(pod_id=1, amount=1000, location='here')
        self.assertFalse(result)

    def test_5_add_feedback_to_dose_success(self):
        print(f'Test: add feedback to dose - success')
        description = "its nice"
        rating = 10
        d_id = 1
        result = self.consumer1.provide_feedback(dosing_id=d_id, feedback_rating=rating, feedback_description=description)
        self.assertTrue(result, "provide_feedback method failed")
        past_dosings = [dose for dose in self.consumer1.dosing_history if dose.id == d_id]
        self.assertTrue(past_dosings, "no dosing after provide_feedback method")
        feedback = past_dosings[0].feedback
        self.assertTrue(feedback, "no dosing after provide_feedback method")
        self.assertTrue(feedback.description == description and feedback.rating == rating, "feedback doesnt match test input args")

    def test_6_add_feedback_to_dose_fail1(self):
        print(f'Test: add feedback to dose - fail:')
        print(f'\t wrong dosing id')
        description = "its nice"
        rating = 10
        d_id = 100
        result = self.consumer1.provide_feedback(dosing_id=d_id, feedback_rating=rating,
                                                 feedback_description=description)
        self.assertFalse(result, "provide_feedback method failed successfully")

    def test_7_add_feedback_to_dose_fail2(self):
        print(f'Test: add feedback to dose - fail:')
        print(f'\t no dosing history records')
        self.consumer1.dosing_history = []
        description = "its nice"
        rating = 10
        d_id = 1
        result = self.consumer1.provide_feedback(dosing_id=d_id, feedback_rating=rating,
                                                 feedback_description=description)
        self.assertFalse(result, "provide_feedback method failed successfully")


if __name__ == '__main__':
    unittest.main()
