from dal.DummyMapper import DummyMapper
from dal.IMapper import IMapper
from dal.Util import DataAccessError
from domain.common.Util import AppOperationError
from domain.medicalCenter.Consumer import Consumer

import logging



class MedicalCenter:

    def __init__(self, mapper: IMapper) -> None:
        self.object_mapper: IMapper = mapper
        self.logger = logging.getLogger('domain.MedicalCenter')
        handler = logging.FileHandler('../../../../domain.log')  # make more generic with a local logging module
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("here!!")
        pass

# consumer related interface

    async def get_consumer(self, consumer_id):
        try:
            consumer = await self.object_mapper.get_consumer(consumer_id)
        except DataAccessError as e:
            self.logger.debug(str(e))
            err_str = f'Error: consumer [{consumer_id}] is not registered in the system.'
            self.logger.info(err_str)
            raise AppOperationError(err_str)
        if not consumer:
            err_str = f'Error: consumer [{consumer_id}] is not registered in the system.'
            raise AppOperationError(err_str)
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
            self.logger.debug(str(e))
            err_str = f'Error: consumer [{consumer_id}] unable to dose from pod [{pod_id}] - with amount [{amount}].'
            self.logger.error(err_str)
            raise AppOperationError(err_str)
        await self.object_mapper.update_consumer(consumer)


    async def consumer_get_consumer_pods(self,consumer_id):
        consumer = await self.get_consumer(consumer_id)
        pods = await consumer.get_pods()
        return pods

    async def consumer_provide_feedback(self, consumer_id, dosing_id, feedback_rating, feedback_description):
        consumer = await self.get_consumer(consumer_id)
        try:
            await consumer.provide_feedback(dosing_id, feedback_rating, feedback_description)
        except ValueError as e:
            err_str = f'Error: consumer [{consumer_id}] unable to provide feedback for dosing [{dosing_id}].'
            self.logger.error(err_str)
            raise AppOperationError(err_str)
        await self.object_mapper.update_consumer(consumer)


    async def consumer_register_pod(self, consumer_id, pod_type):
        consumer = await self.get_consumer(consumer_id)
        try:
            await consumer.register_pod(pod_type=pod_type)
        except ValueError as e:
            err_str = f'Error: consumer [{consumer_id}] unable to register pod.'
            self.logger.error(err_str)
            raise AppOperationError(err_str)
        await self.object_mapper.update_consumer(consumer)


    async def consumer_register_dispenser(self, consumer_id, dispenser_serial_number):
        consumer = await self.get_consumer(consumer_id)
        try:
            await consumer.register_dispenser(dispenser_serial_number)
        except ValueError as e:
            err_str = f'Error: consumer [{consumer_id}] unable to register dispenser [{dispenser_serial_number}].'
            self.logger.error(err_str)
            raise AppOperationError(err_str)
        await self.object_mapper.update_consumer(consumer)


    async def consumer_get_recommendation(self, consumer_id):
        consumer = await self.get_consumer(consumer_id)
        try:
            recommendation_res = await consumer.get_recommendation(None)
        except Exception as e:
            err_str = f'Error: consumer [{consumer_id}] unable to get recommendation.'
            self.logger.error(err_str)
            raise AppOperationError(err_str)
        await self.object_mapper.update_consumer(consumer)
        return recommendation_res


    async def register_consumer(self, user_id: int):
        # @TODO: Check if User(!) already registered
        # @TODO: add the rest of the fields of new_consumer
        new_consumer = Consumer()
        result = await self.object_mapper.add_consumer(new_consumer)
        # @TODO: check that adding consumer was successful
        return result

