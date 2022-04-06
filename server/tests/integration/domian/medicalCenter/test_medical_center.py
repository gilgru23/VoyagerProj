import unittest

from domain.medicalCenter.Consumer import Consumer
from domain.medicalCenter.MedicalCenter import MedicalCenter


class TestMedicalCenter(unittest.IsolatedAsyncioTestCase):

    medical_center = MedicalCenter()

    def setUp(self):
        pass

    async def test_example(self):
        await self.medical_center.get_consumer(1)
        self.assertTrue(True)


    async def test_0_consumer_get_dosing_history(self):
        consumer: Consumer = await self.medical_center.get_consumer(1)
        self.assertTrue(consumer is not None)
        result = await consumer.get_dosage_history()
        self.assertTrue(result is not None)

