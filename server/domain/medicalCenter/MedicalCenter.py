from dal.DummyMapper import DummyMapper
from dal.IMapper import IMapper
from domain.medicalCenter.Consumer import Consumer
import domain.common.Result as res


# @TODO: make this class a singleton (?)


class MedicalCenter:

    def __init__(self) -> None:
        self.object_mapper: IMapper = DummyMapper()
        pass


# consumer related interface
    def consumer_error(self,consumer_id):
        return False, f"Error : consumer [{consumer_id}] not found!"

    async def get_consumer(self, consumer_id):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        if consumer is None:
            return self.consumer_error(consumer_id)
        return consumer

    async def get_consumer_history(self, consumer_id, filters):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        if consumer is None:
            return self.consumer_error(consumer_id)
        history = await consumer.get_dosage_history(filters)
        return history

    async def consumer_dose(self,consumer_id, pod_id, amount: float, location):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        if consumer is None:
            return self.consumer_error(consumer_id)
        # @TODO: add a call (await) to IMapper (when adding DAL)
        pass

    async def consumer_get_consumer_pods(self,consumer_id):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        if consumer is None:
            return self.consumer_error(consumer_id)
        history = await consumer.get_pods()
        return history

    async def consumer_provide_feedback(self, consumer_id, dosing_id, feedback_rating, feedback_description):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        if consumer is None:
            return self.consumer_error(consumer_id)
        result = await consumer.provide_feedback(dosing_id, feedback_rating, feedback_description)
        # @TODO: add a call (await) to IMapper to update feedback situation (when adding DAL)
        return result

    async def consumer_register_pod(self, consumer_id, pod_type):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        if consumer is None:
            return self.consumer_error(consumer_id)
        result = await consumer.register_pod(pod_type=pod_type)
        # @TODO: add a call (await) to IMapper to update pod situation (when adding DAL)
        return result

    async def consumer_register_dispenser(self, consumer_id, dispenser_serial_number):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        if consumer is None:
            return self.consumer_error(consumer_id)
        result = await consumer.register_dispenser(dispenser_serial_number)
        # @TODO: add a call (await) to IMapper to update dispenser registration (when adding DAL)
        return result

    async def consumer_get_recommendation(self, consumer_id):
        consumer = await self.object_mapper.get_consumer(consumer_id)
        if consumer is None:
            return self.consumer_error(consumer_id)
        result = await consumer.get_recommendation(None)
        return result

    async def register_consumer(self, user_id: int):
        consumer = await self.object_mapper.get_consumer(user_id)
        if consumer:
            return res.failure("user is already a consumer")
        await self.object_mapper.add_consumer(user_id)
        #todo: check that adding consumer was successful
        return res.success()