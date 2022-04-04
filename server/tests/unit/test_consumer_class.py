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
        dosing_output = self.consumer1.get_dosage_history()
        for d_out,d_hist in zip(dosing_output, self.consumer1.dosing_history):
            self.assertEqual(d_out,d_hist)


    def test_1_dose_success(self):
        self.consumer1.dose(pod_id=1, amount=42.5,location='here')
        # check a new dosing was added to history at the front of the list
        new_dosing: Dosing = self.consumer1.dosing_history[0]
        self.assertEqual(new_dosing.pod_id, 1)
        self.assertEqual(new_dosing.amount, 42.5)
        # check the pod remainder changed according to the amount of substance dosed
        pod: Pod = self.consumer1.get_pod_by_id(1)
        self.assertEqual(pod.remainder, 100 - 42.5)

if __name__ == '__main__':
    unittest.main()
