from dal.DummyMapper import DummyMapper
from dal.IMapper import IMapper
from domain.medicalCenter.Consumer import Consumer


# @TODO: make this class a singleton (?)


class MedicalCenter:

    def __init__(self) -> None:
        self.object_mapper: IMapper = DummyMapper()
        pass


# consumer related interface
    async def get_consumer(self, consumer_id):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        if consumer is None:
            return (False, f"Error : consumer [{consumer_id}] not found!")
        return consumer

    async def get_consumer_history(self, consumer_id, filters):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        history = consumer.get_dosage_history(filters)
        return history

    async def consumer_dose(self,pod_id, amount: float, location):
        pass

    async def consumer_get_consumer_pods(self,consumer_id):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        history = consumer.get_pods()
        return history

    async def consumer_provide_feedback(self, consumer_id, dosing_id, feedback_rating, feedback_description):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        result = consumer.provide_feedback(dosing_id, feedback_rating, feedback_description)
        return result

    async def consumer_register_pod(self, consumer_id, pod_type):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        result = consumer.register_pod(pod_type=pod_type)
        # @TODO: add a call (await) to IMapper to update pod situation (when adding DAL)
        return result

    async def consumer_register_dispenser(self, consumer_id, dispenser_serial_number):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        result = consumer.register_dispenser(dispenser_serial_number)
        # @TODO: add a call (await) to IMapper to update dispenser registration (when adding DAL)
        return result

    async def consumer_get_recommendation(self, consumer_id):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        result = consumer.get_recommendation(None)
        return result

