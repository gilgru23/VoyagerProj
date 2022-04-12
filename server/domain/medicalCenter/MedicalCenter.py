from dal.DummyMapper import DummyMapper
from dal.IMapper import IMapper
from dal.Util import DataAccessError
from domain.common.Util import AppOperationError
from domain.medicalCenter.Consumer import Consumer


# @TODO: make this class a singleton (?)


class MedicalCenter:

    def __init__(self, mapper: IMapper) -> None:
        self.object_mapper: IMapper = mapper
        pass


# consumer related interface

    async def get_consumer(self, consumer_id):
        try:
            consumer = await self.object_mapper.get_consumer(consumer_id)
        except DataAccessError as e:
            # @TODO: log the exception e
            raise AppOperationError('some DB exception')
        if not consumer:
            # @TODO: log 'consumer was not found'
            raise AppOperationError(f'Error: consumer [{consumer_id}] is not registered in the system')
        return consumer

    async def get_consumer_history(self, consumer_id, filters):
        consumer = await self.get_consumer(consumer_id)
        history = await consumer.get_dosage_history(filters)
        return history

    async def consumer_dose(self,consumer_id, pod_id, amount: float, location):
        consumer = await self.get_consumer(consumer_id)
        try:
            await consumer.dose(pod_id=pod_id, amount=amount, location=location)
        except ValueError as e:
            # @TODO: log the exception e
            raise AppOperationError('')

        # @TODO: add a call (await) to IMapper (when adding DAL)


    async def consumer_get_consumer_pods(self,consumer_id):
        consumer = await self.get_consumer(consumer_id)
        pods = await consumer.get_pods()
        return pods

    async def consumer_provide_feedback(self, consumer_id, dosing_id, feedback_rating, feedback_description):
        consumer = await self.get_consumer(consumer_id)
        try:
            await consumer.provide_feedback(dosing_id, feedback_rating, feedback_description)
        except ValueError as e:
            # @TODO: log the exception e
            raise AppOperationError('')
        # @TODO: add a call (await) to IMapper to update feedback situation (when adding DAL)


    async def consumer_register_pod(self, consumer_id, pod_type):
        consumer = await self.get_consumer(consumer_id)
        try:
            await consumer.register_pod(pod_type=pod_type)
        except ValueError as e:
            # @TODO: log the exception e
            raise AppOperationError('')
        # @TODO: add a call (await) to IMapper to update pod situation (when adding DAL)


    async def consumer_register_dispenser(self, consumer_id, dispenser_serial_number):
        consumer = await self.get_consumer(consumer_id)
        try:
            await consumer.register_dispenser(dispenser_serial_number)
        except ValueError as e:
            # @TODO: log the exception e
            raise AppOperationError('')
        # @TODO: add a call (await) to IMapper to update dispenser registration (when adding DAL)

    async def consumer_get_recommendation(self, consumer_id):
        consumer = await self.get_consumer(consumer_id)
        try:
            recommendation_res = await consumer.get_recommendation(None)
        except Exception as e:
            # @TODO: log the exception e
            raise AppOperationError('')
        return recommendation_res

    async def register_consumer(self, user_id: int):
        # @TODO: Check if User(!) already registered
        # @TODO: add the rest of the fields of new_consumer
        new_consumer = Consumer()
        result = await self.object_mapper.add_consumer(new_consumer)
        # @TODO: check that adding consumer was successful
        return result

