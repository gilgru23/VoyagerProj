import unittest

from domain.medicalCenter.MedicalCenter import MedicalCenter


class TestMedicalCenter(unittest.IsolatedAsyncioTestCase):

    medical_center = MedicalCenter()

    def setUp(self):
        pass

    async def test_example(self):
        await self.medical_center.get_consumer(1)
        self.assertTrue(True)


