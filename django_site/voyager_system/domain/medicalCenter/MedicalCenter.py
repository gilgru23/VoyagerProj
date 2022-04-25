from voyager_system.dal.IMapper import IMapper
from voyager_system.dal.Util import DataAccessError
from voyager_system.data_access import IStorage
from voyager_system.domain.common.Util import AppOperationError
from voyager_system.domain.medicalCenter.Consumer import Consumer

from voyager_system.data_access.DatabaseProxy import DatabaseProxy as db

from common import Logger




class MedicalCenter:

    def __init__(self,mapper:IMapper, db_proxy: IStorage) -> None:
        self.object_mapper: IMapper = mapper
        self.db = db_proxy
        self.logger = Logger.get_logger('Domain','MedicalCenter')
        self.logger.debug("here!!")
        pass


# consumer related interface

    # retrieves a consumer from database (or cache) by id
    # returns the consumer if found
    # else throws an AppOperationError exception
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

    # retrieves the dosing history of the consumer (consumer_id)
    # returns a list of dosings if found
    # throws an AppOperationError exception if consumer was not found (see get_consumer)
    async def get_consumer_history(self, consumer_id, filters):
        consumer = await self.get_consumer(consumer_id)
        history = await consumer.get_dosage_history(filters)
        return history

    # update a dosing of the consumer (consumer_id) -
    # adds dosing to history and changes the remainder of the relevant pod
    # throws an AppOperationError exception if consumer was not found (see get_consumer) or if
    # dosing was not possible with the given parameters (pod_id, amount)
    async def consumer_dose(self,consumer_id, pod_id, amount: float, location):
        consumer = await self.get_consumer(consumer_id)
        # try:
        await consumer.dose(pod_id=pod_id, amount=amount, location=location)
        # except AppOperationError as e:
        #     self.logger.debug(str(e))
        #     err_str = f'Error: consumer [{consumer_id}] unable to dose from pod [{pod_id}] - with amount [{amount}].'
        #     self.logger.error(err_str)
        #     raise AppOperationError(err_str)
        await self.object_mapper.update_consumer(consumer)

    # retrieves a shallow copy of all of the pods registered to the consumer (consumer_id)
    # throws an AppOperationError exception if consumer was not found (see get_consumer)
    async def consumer_get_consumer_pods(self,consumer_id):
        consumer = await self.get_consumer(consumer_id)
        pods = await consumer.get_pods()
        return pods

    # update the feedback of a consumer's (consumer_id) past dosing -
    # sets the feedback to a dosing (dosing_id) in consumer's dosing history
    # throws an AppOperationError exception if consumer was not found (see get_consumer) or if
    # the dosing (dosing_id) is not found in consumer's dosing-history.
    async def consumer_provide_feedback(self, consumer_id, dosing_id, feedback_rating, feedback_description):
        consumer = await self.get_consumer(consumer_id)
        await consumer.provide_feedback(dosing_id, feedback_rating, feedback_description)
        await self.object_mapper.update_consumer(consumer)

    # registers a pod of the specified type (pod_type) and id (pod_id) to the consumer's (consumer_id)
    # throws an AppOperationError exception if consumer was not found (see get_consumer)
    async def consumer_register_pod(self, consumer_id, pod_id, pod_type):
        consumer = await self.get_consumer(consumer_id)
        await consumer.register_pod(pod_id=pod_id, pod_type=pod_type)
        await self.object_mapper.update_consumer(consumer)

    # registers a dispenser of the specified serial number (serial_number) to the consumer (consumer_id)
    # throws an AppOperationError exception if consumer was not found (see get_consumer)
    async def consumer_register_dispenser2(self, consumer_id, dispenser_serial_number):
        consumer = await self.get_consumer(consumer_id)
        await consumer.register_dispenser(dispenser_serial_number)
        await self.object_mapper.update_consumer(consumer)

    # deprecated - to be removed
    def consumer_register_dispenser(self, consumer_id, dispenser_serial_number):
        return db.set_dispenser_consumer(dispenser_serial_number, consumer_id)


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

