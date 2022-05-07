from voyager_system.dal_DEPRECATED.IMapper import IMapper
from voyager_system.domain.DatabaseProxy import DatabaseProxy
from voyager_system.common.ErrorTypes import AppOperationError, DataAccessError
from voyager_system.domain.medical_center.Consumer import Consumer
from voyager_system.domain.medical_center.Pod import *

from voyager_system.common import Logger


# imports for test purposes
# from voyager_system.data_access.DatabaseProxy import DatabaseProxy
# import voyager_system.data_access.database as database


class MedicalCenter:
    # mapper is deprecated
    def __init__(self, db_proxy: DatabaseProxy, mapper: IMapper = None) -> None:
        self.object_mapper: IMapper = mapper
        self.db = db_proxy
        self.notifier = None
        self.logger = Logger.get_logger('Domain', 'MedicalCenter')
        pass

    # region Consumer
    # consumer related interface


    # async def get_consumer2(self, consumer_id):
    #     """retrieves a consumer from database (or cache) by id
    #
    #     :param consumer_id: id of the consumer
    #     :return: Consumer object.
    #     :raise  AppOperationError: throws exception if consumer was not found
    #     """
    #     try:
    #         consumer = await self.object_mapper.get_consumer(consumer_id)
    #     except DataAccessError as e:
    #         self.logger.debug(str(e))
    #         err_str = f'Error: consumer [id: {consumer_id}] is not registered in the system.'
    #         self.logger.info(err_str)
    #         raise AppOperationError(err_str)
    #     if not consumer:
    #         err_str = f'Error: consumer [id: {consumer_id}] is not registered in the system.'
    #         raise AppOperationError(err_str)
    #     self.logger.debug(f' retrieved consumer [id: {consumer_id}] from db proxy')
    #     return consumer

    def get_consumer(self, consumer_id) -> Consumer:
        """retrieves a consumer from database (or cache) by id

        :param consumer_id: id of the consumer
        :return: Consumer object.
        :raise  AppOperationError: throws exception if consumer was not found
        """
        try:
            consumer = self.db.get_consumer(consumer_id)
        except DataAccessError as e:
            self.logger.debug(str(e))
            err_str = f'Error: getting consumer - consumer [id: {consumer_id}] .\n' + str(e)
            self.logger.info(err_str)
            raise e
        if not consumer:
            err_str = f'Error: getting consumer - consumer [id: {consumer_id}] is not registered in the system.'
            raise AppOperationError(err_str)
        self.logger.debug(f' retrieved consumer [id: {consumer_id}] from db proxy')
        return consumer

    async def get_consumer_dosing_history(self, consumer_id, filters=None):
        """retrieves the dosing history of the consumer (consumer_id)

        :param consumer_id: id of the consumer
        :param filters: list of filters to apply on the returned list
        :return: list of Dosings, if found.
        :raise AppOperationError: throws exception if consumer was not found (see get_consumer)
        """

        consumer = await self.get_consumer(consumer_id)
        history = await consumer.get_dosage_history(filters)
        # log changes
        self.logger.debug(f"retrieved consumer's [id: {consumer_id}] dosing history")
        return history

    async def consumer_dose(self, consumer_id, pod_id, amount: float, location):
        """updates a dosing of the consumer-

        adds dosing to history and changes the remainder of the relevant pod

        :param consumer_id: id of the consumer
        :param pod_id: id of the consumer from which a dose is taken
        :param amount: the amount of substance dosed (float)
        :param location: the physical location at which the dosing took place
        :return: None
        :raise AppOperationError: throws exception if consumer was not found (see get_consumer) or
                if dosing was not possible with the given parameters (pod_id, amount)
        """
        consumer = await self.get_consumer(consumer_id)
        await consumer.dose(pod_id=pod_id, amount=amount, location=location)
        await self.db.update_consumer(consumer)
        self.logger.info(f"consumer [id: {consumer_id}] dosed from pod [pod_id: {pod_id}] - with amount [{amount}]")

    async def get_consumer_pods(self, consumer_id):
        """retrieves a shallow copy of all of the pods registered to the consumer

        :param consumer_id: id of the consumer
        :return: None
        :raise AppOperationError: exception if consumer was not found (see get_consumer)
        """
        consumer = await self.get_consumer(consumer_id)
        pods = await consumer.get_pods()
        self.logger.debug(f"retrieved consumer's [id: {consumer_id}] registered pods")
        return pods

    async def consumer_provide_feedback(self, consumer_id, dosing_id, feedback_rating, feedback_description):
        """update the feedback of a consumer's past dosing-
        sets the feedback to a dosing (dosing_id) in consumer's dosing history

        :param consumer_id: id of the consumer
        :param dosing_id: id of the dosing occurrence
        :param feedback_rating: the rating given by the user as feedback (int [1,10])
        :param feedback_description: text description of the feedback (string)
        :return: None
        :raise AppOperationError: throws exception if consumer was not found (see get_consumer) or
                if the dosing (dosing_id) is not found in consumer's dosing-history
        """
        consumer = await self.get_consumer(consumer_id)
        await consumer.provide_feedback(dosing_id, feedback_rating, feedback_description)
        await self.db.update_consumer(consumer)
        self.logger.info(f"consumer [id: {consumer_id}] added feedback to dosing [id: {dosing_id}]")

    def consumer_register_pod(self, consumer_id: int, pod_id: int, pod_type: int):
        """registers a pod of the specified id and type to the consumer

        :param consumer_id: int - id of the consumer
        :param pod_id: int - id of the consumer from which a dose is taken
        :param pod_type: the type of the pod (PodType object)
        :return: None
        :raise AppOperationError: throws exception if consumer was not found (see get_consumer)
        """
        consumer = self.get_consumer(consumer_id)
        ptype = self.get_pod_type_from_typeId(pod_type)
        await consumer.register_pod(pod_id=pod_id, pod_type=ptype)
        self.db.update_consumer(consumer)
        self.logger.info(f"consumer [id: {consumer_id}] registered pod [id: {pod_id}]")

    async def consumer_register_dispenser2(self, consumer_id, dispenser_serial_number):
        """registers a dispenser of the specified serial number to the consumer

        :param consumer_id: id of the consumer
        :param dispenser_serial_number: serial number of the dispenser
        :return: None
        :raise AppOperationError: throws exception if consumer was not found (see get_consumer)
        """
        consumer = await self.get_consumer(consumer_id)
        await consumer.register_dispenser(dispenser_serial_number)
        await self.object_mapper.update_consumer(consumer)
        self.logger.info(f"consumer [id: {consumer_id}] registered dispenser [serial #: {dispenser_serial_number}]")

    # deprecated - to be removed
    # @staticmethod
    def consumer_register_dispenser(self, consumer_id, dispenser_serial_number):
        # new_db = DatabaseProxy(database)
        return self.db.set_dispenser_consumer(dispenser_serial_number=dispenser_serial_number, consumer_id=consumer_id)

    async def consumer_get_recommendation(self, consumer_id):
        consumer = await self.get_consumer(consumer_id)
        try:
            recommendation_res = await consumer.get_recommendation(None)
        except Exception as e:
            err_str = f'Error: consumer [id: {consumer_id}] unable to get recommendation.'
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

    # endregion Consumer


    # region Pods
    def get_pod_type_from_typeId(self, type_id: int) -> PodType:
        return PodType(-1,-1,"Nothing")
    # todo: check in MarketPlace
    def validate_pod(self, pod_id: int) -> Pod:
        return Pod(-1,self.get_pod_type_from_typeId(-1))

    # endregion Pods


