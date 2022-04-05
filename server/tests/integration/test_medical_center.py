import unittest

from domain.medicalCenter.MedicalCenter import MedicalCenter


class TestMedicalCenter(unittest.TestCase):

    medical_center = MedicalCenter()

    def setUp(self):
        pass

    def test_example(self):
        self.medical_center.get_consumer(1)
        self.assertTrue(True)


