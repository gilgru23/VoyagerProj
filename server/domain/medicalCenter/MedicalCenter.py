from dal.DummyMapper import DummyMapper
from dal.IMapper import IMapper
from domain.medicalCenter.Consumer import Consumer
import domain.common.Result as Res


# @TODO: make this class a singleton (?)


class MedicalCenter:

    def __init__(self, mapper: IMapper) -> None:
        self.object_mapper: IMapper = mapper
        pass


# consumer related interface

    async def get_consumer(self, consumer_id):
        consumer_res = await self.object_mapper.get_consumer(consumer_id)
        if Res.is_failure(consumer_res):
            return consumer_res
        return consumer_res

    async def get_consumer_history(self, consumer_id, filters):
        consumer_res = await self.object_mapper.get_consumer(consumer_id)
        if Res.is_failure(consumer_res):
            return consumer_res
        consumer = Res.get_value(consumer_res)
        history = await consumer.get_dosage_history(filters)
        return history

    async def consumer_dose(self,consumer_id, pod_id, amount: float, location):
        consumer_res = await self.object_mapper.get_consumer(consumer_id)
        if Res.is_failure(consumer_res):
            return consumer_res
        consumer = Res.get_value(consumer_res)
        dose_res = await consumer.dose(pod_id=pod_id,amount=amount,location=location)
        # @TODO: add a call (await) to IMapper (when adding DAL)
        return dose_res

    async def consumer_get_consumer_pods(self,consumer_id):
        consumer_res = await self.object_mapper.get_consumer(consumer_id)
        if Res.is_failure(consumer_res):
            return consumer_res
        consumer = Res.get_value(consumer_res)
        history_res = await consumer.get_pods()
        return history_res

    async def consumer_provide_feedback(self, consumer_id, dosing_id, feedback_rating, feedback_description):
        consumer_res = await self.object_mapper.get_consumer(consumer_id)
        if Res.is_failure(consumer_res):
            return consumer_res
        consumer = Res.get_value(consumer_res)
        feedback_res = await consumer.provide_feedback(dosing_id, feedback_rating, feedback_description)
        # @TODO: add a call (await) to IMapper to update feedback situation (when adding DAL)
        return feedback_res

    async def consumer_register_pod(self, consumer_id, pod_type):
        consumer_res = await self.object_mapper.get_consumer(consumer_id)
        if Res.is_failure(consumer_res):
            return consumer_res
        consumer = Res.get_value(consumer_res)
        result = await consumer.register_pod(pod_type=pod_type)
        # @TODO: add a call (await) to IMapper to update pod situation (when adding DAL)
        return result

    async def consumer_register_dispenser(self, consumer_id, dispenser_serial_number):
        consumer_res = await self.object_mapper.get_consumer(consumer_id)
        if Res.is_failure(consumer_res):
            return consumer_res
        consumer = Res.get_value(consumer_res)
        result = await consumer.register_dispenser(dispenser_serial_number)
        # @TODO: add a call (await) to IMapper to update dispenser registration (when adding DAL)
        return result

    async def consumer_get_recommendation(self, consumer_id):
        consumer_res = await self.object_mapper.get_consumer(consumer_id)
        if Res.is_failure(consumer_res):
            return consumer_res
        consumer = Res.get_value(consumer_res)
        recommendation_res = await consumer.get_recommendation(None)
        return recommendation_res

    async def register_consumer(self, user_id: int):
        consumer_res = await self.object_mapper.get_consumer(user_id)
        if Res.is_successful(consumer_res):
            return Res.failure(f"Error: register consumer: user [{user_id}] is already a registered consumer")
        # @TODO: add the rest of the fields of new_consumer
        new_consumer = Consumer()
        result = await self.object_mapper.add_consumer(new_consumer)
        # @TODO: check that adding consumer was successful
        return result

