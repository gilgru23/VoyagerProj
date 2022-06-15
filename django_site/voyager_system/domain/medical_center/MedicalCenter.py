

from voyager_system.common.DateTimeFormats import date_to_str, date_time_to_str
from voyager_system.data_access.DatabaseProxy import DatabaseProxy
from voyager_system.common.ErrorTypes import AppOperationError, DataAccessError
from voyager_system.domain.marketplace.MarketPlace import MarketPlace
from voyager_system.domain.medical_center.Consumer import Consumer
from voyager_system.domain.medical_center.Dispenser import Dispenser
from voyager_system.domain.medical_center.Dosing import Dosing, Feedback
from voyager_system.domain.medical_center.Pod import *

from voyager_system.common import Logger


# imports for test purposes
# from voyager_system.data_access.DatabaseProxy import DatabaseProxy
# import voyager_system.data_access.database as database


# noinspection SpellCheckingInspection
class MedicalCenter:
    def __init__(self, db_proxy: DatabaseProxy, marketplace=None, notifier=None) -> None:
        self.db = db_proxy
        self.marketpalce: MarketPlace = marketplace
        self.notifier = notifier
        self.logger = Logger.get_logger('Domain', 'MedicalCenter')
        pass

    # region Consumer

    # consumer related interface

    def get_consumer(self, consumer_id) -> Consumer:
        """retrieves a consumer from database (or cache) by id

        :param consumer_id: id of the consumer
        :return: Consumer object.
        :raise  AppOperationError: throws exception if the consumer is not registered
        :raise DataAccessError: throws exception if db was not able to get consumer
        """
        try:
            consumer = self.db.get_consumer(consumer_id)
        except DataAccessError as e:
            err_str = f'Error: getting consumer - consumer [id: {consumer_id}] .\n' + str(e)
            self.logger.info(err_str)
            raise e
        if not consumer:
            err_str = f'Error: getting consumer - consumer [id: {consumer_id}] is not registered in the system.'
            self.logger.debug(err_str)
            raise AppOperationError(err_str)
        self.logger.debug(f' retrieved consumer [id: {consumer_id}] from db proxy')
        return consumer

    def get_consumer_dosing_history(self, consumer_id, filters=None):
        """retrieves the dosing history of the consumer (consumer_id). Dosing do not contain Feedback

        :param consumer_id: id of the consumer
        :param filters: list of filters to apply on the returned list
        :return: A List of Dictionaries representing past Dosings registered to the consumer.
        :raise AppOperationError: throws exception if consumer was not found (see get_consumer)
        :raise DataAccessError: throws exception if db was not able to get consumer
        """

        def dosing_to_dict(dosing: Dosing, pod_type: str):
            return {'dosing_id': dosing.id,'pod_serial_number': dosing.pod_serial_number, 'pod_type_name': pod_type,
                    'amount': dosing.amount, 'time': date_time_to_str(dosing.time), 'latitude': dosing.latitude,
                    'longitude': dosing.longitude}

        def get_pod_type(pod_serial_num: str):
            if pod_serial_num in type_names:
                return type_names[pod_serial_num]
            pod = self.db.get_pod(pod_serial_num)
            type_name = pod.type_name
            type_names[pod_serial_num] = type_name
            return type_name

        type_names = dict()
        dosings = self.db.get_consumer_dosing(consumer_id)
        # pod_serials = {dosing.pod_serial_number for dosing in dosings}
        history = [dosing_to_dict(d, get_pod_type(d.pod_serial_number)) for d in dosings]
        self.logger.debug(f"retrieved consumer's [id: {consumer_id}] dosing history")
        return history

    def consumer_dose(self, consumer_id, pod_serial_num: str, amount: float, time, latitude, longitude):
        """
        updates a dosing of the consumer-
        adds dosing to history and changes the remainder of the relevant pod

        :param consumer_id: int - id of the consumer
        :param pod_serial_num: str - serial number of the pod from which a dose is taken
        :param amount: float - the amount of substance dosed (float)
        :param time: the time the dosing took place
        :param latitude: the physical location at which the dosing took place
        :param longitude: the physical location at which the dosing took place
        :return: None
        :raise AppOperationError: throws exception if consumer was not found (see get_consumer) or
                if dosing was not possible with the given parameters (pod_serial_num, amount)
        :raise DataAccessError: throws exception if db was not able to get the consumer, it's pods or past dosings
        """
        consumer = self.get_consumer(consumer_id)
        consumer.pods = self.db.get_consumer_pods(consumer_id)
        consumer.dosing_history = self.db.get_consumer_dosing(consumer_id)
        new_dosing: Dosing = consumer.dose(pod_serial_number=pod_serial_num, amount=amount, time_str=time,
                                           latitude=latitude, longitude=longitude)
        pod: Pod = consumer.get_pod_by_serial_number(pod_serial_num)
        self.db.add_dosing(new_dosing)
        self.db.update_pod(pod, consumer_id)
        self.logger.info(
            f"consumer [id: {consumer_id}] dosed from pod [serial number: {pod_serial_num}] - with amount [{amount}]")

    def get_consumer_dispensers(self, consumer_id):
        """
        retrieves a list of dictionaries representing all of the dispensers registered to the consumer

        :param consumer_id: id of the consumer
        :return: A List of Dictionaries representing dispensers registered to the consumer
        :raise AppOperationError: exception if consumer was not found (see get_consumer)
        :raise DataAccessError: throws exception if db was not able to retrieve consumer or dispensers
        """
        dispensers = self.db.get_consumer_dispensers(consumer_id)

        def disp_to_dict(disp: Dispenser):
            return {'serial_number': disp.serial_number, 'version': disp.version,
                    'registration_date': date_to_str(disp.registration_date)}

        dispenser_dicts = [disp_to_dict(disp) for disp in dispensers]
        self.logger.debug(f"retrieved consumer's [id: {consumer_id}] registered dispensers")
        return dispenser_dicts

    def get_consumer_pods(self, consumer_id):
        """
        retrieves a list of dictionaries representing all of the pods registered to the consumer

        :param consumer_id: id of the consumer
        :return: A List of Dictionaries representing pods registered to the consumer
        :raise AppOperationError: exception if consumer was not found (see get_consumer)
        :raise DataAccessError: throws exception if db was not able to retrieve consumer or pods
        """

        def pod_to_dict(pod: Pod):
            return {'serial_number': pod.serial_number, 'remainder': pod.remainder, 'type_name': pod.type_name}

        pods = self.db.get_consumer_pods(consumer_id)
        pod_dicts = [pod_to_dict(pod) for pod in pods]
        self.logger.debug(f"retrieved consumer's [id: {consumer_id}] registered pods")
        return pod_dicts

    @staticmethod
    def sort_consumer_feedbacks(consumer, feedbacks):
        dosings = {dose.id: dose for dose in consumer.dosing_history}
        for feed in feedbacks:
            dosings[feed.dosing_id].feedback = feed

    def consumer_provide_feedback(self, consumer_id, dosing_id, feedback_rating, feedback_comment):
        """
        update the feedback of a consumer's past dosing-
        sets the feedback to a dosing (dosing_id) in consumer's dosing history.
        (dosing must not already have a feedback proiveded)

        :param consumer_id: int - id of the consumer
        :param dosing_id: int - id of the dosing occurrence
        :param feedback_rating: int - the rating given by the user as feedback [1 - 10]
        :param feedback_comment: str - text description of the feedback
        :return: None
        :raise AppOperationError: throws exception if consumer was not found (see get_consumer) or
                if dosing was not found in consumer's dosing-history or dosing already has a feedback provided
        :raise DataAccessError: throws exception if db was not able to get the consumer or it's past dosings
        """

        consumer = self.get_consumer(consumer_id)
        consumer.dosing_history = self.db.get_consumer_dosing(consumer_id)
        past_feedbacks = self.db.get_feedbacks_for_consumer(consumer_id)
        self.sort_consumer_feedbacks(consumer,past_feedbacks)
        feedback: Feedback = consumer.provide_feedback(dosing_id, feedback_rating, feedback_comment)
        self.db.add_feedback(feedback, dosing_id)
        self.logger.info(f"consumer [id: {consumer_id}] added feedback to dosing [id: {dosing_id}]")

    def get_feedback_for_dosing(self, consumer_id, dosing_id):
        """
        retrieves the Feedback the Consumer (consumer_id) provided for Dosing (dosing_id)

        :param consumer_id: int - id of the consumer requestiong the feedback
        :param dosing_id: int - id of the dosing for which the feedback was provided
        :return: A Dictionary representing the feedback.
        :raise AppOperationError: throws exception if consumer, dosings or feedback were not found
        :raise DataAccessError: throws exception if db was not able to get consumer, dosings or feedback
        """

        def feedback_to_dict(feed: Feedback):
            return {'dosing_id': feed.dosing_id, 'time': date_time_to_str(feed.time), 'rating': feed.rating, 'comment':feed.comment}

        consumer = self.get_consumer(consumer_id)
        consumer.dosing_history = self.db.get_consumer_dosing(consumer_id)
        past_feedbacks = self.db.get_feedbacks_for_consumer(consumer_id)
        self.sort_consumer_feedbacks(consumer,past_feedbacks)
        dosing = consumer.get_dosing_by_id(dosing_id)
        if dosing is None:
            raise AppOperationError(f"Error: consumer [{consumer_id}] doesn't have a dosing with matching dosing_id [{dosing_id}]")
        feedback = self.db.get_feedback_for_dosing(dosing_id)
        if feedback is None:
            raise AppOperationError(
                f"Error: consumer [{consumer_id}] doesn't have a feedback provided for dosing with dosing_id [{dosing_id}]")
        self.logger.debug(f"retrieved consumer's [id: {consumer_id}] feedback for dosing [id: {dosing_id}]")
        return feedback_to_dict(feedback)

    def consumer_register_pod(self, consumer_id: int, pod_serial_num: str, pod_type_name: str):
        """registers a pod of the specified id and type to the consumer

        :param consumer_id: int - id of the consumer
        :param pod_serial_num: string - serial-number of the pod from which a dose is taken
        :param pod_type_name: string - the type of the pod (PodType-objects' name-field)
        :return: None
        :raise AppOperationError: throws exception if the consumer is not registered
        :raise DataAccessError: throws exception if db was not able to get consumer
        """
        consumer = self.get_consumer(consumer_id)
        consumer.pods = self.db.get_consumer_pods(consumer_id)
        pod = self.marketpalce.validate_pod(pod_serial_num, pod_type_name)
        consumer.register_pod(pod=pod)
        self.db.update_pod(pod=pod, consumer_id=consumer.id)
        self.logger.info(f"consumer [id: {consumer_id}] registered pod [#: {pod_serial_num}]")

    def consumer_register_dispenser(self, consumer_id, dispenser_serial_number, dispenser_version):
        """registers a dispenser of the specified serial number to the consumer

        :param consumer_id: int - id of the consumer
        :param dispenser_serial_number: string - serial number of the dispenser
        :param dispenser_version: string - the version of the dispenser
        :return: None
        :raise AppOperationError: throws exception if consumer was not found (see get_consumer)
        """
        consumer = self.get_consumer(consumer_id)
        consumer.dispensers = self.db.get_consumer_dispensers(consumer_id)
        dispenser = self.marketpalce.validate_dispenser(serial_num=dispenser_serial_number, version=dispenser_version)
        consumer.register_dispenser(dispenser)
        self.db.update_dispenser(dispenser, consumer_id=consumer_id)
        self.logger.info(f"consumer [id: {consumer_id}] registered dispenser [serial #: {dispenser_serial_number}]")

    def consumer_get_recommendation(self, consumer_id):
        consumer = self.get_consumer(consumer_id)
        try:
            recommendation = None
            # RecommendationServiceAdapter.get_recommendation_for_consumer(consumer)
            raise NotImplementedError()
        except Exception as e:
            err_str = f'Error: consumer [id: {consumer_id}] unable to get recommendation.'
            self.logger.error(err_str)
            raise AppOperationError(err_str)
        return recommendation

    # endregion Consumer


