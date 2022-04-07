import unittest

from domain.medicalCenter.Consumer import Consumer
from domain.medicalCenter.MedicalCenter import MedicalCenter

import domain.common.Result as Res

class TestMedicalCenter(unittest.IsolatedAsyncioTestCase):

    medical_center = MedicalCenter()

    def setUp(self):
        pass

    async def test_example(self):
        await self.medical_center.get_consumer(1)
        self.assertTrue(True)


    async def test_0_consumer_get_dosing_history(self):
        consumer_res = await self.medical_center.get_consumer(1)
        self.assertTrue(Res.is_successful(consumer_res))
        consumer: Consumer = Res.get_value(consumer_res)
        self.assertTrue(consumer is not None)
        history_res = await consumer.get_dosage_history()
        self.assertTrue(Res.is_successful(history_res))
        history = Res.get_value(history_res)
        self.assertTrue(history is not None)

