from django.utils import timezone
from voyager_system.common.DateTimeFormats import parse_string_to_timezone

from voyager_system.domain.system_management.Account import Account
from voyager_system.common.ErrorTypes import AppOperationError
from voyager_system.domain.medical_center.Dispenser import Dispenser
from voyager_system.domain.medical_center.Dosing import *
from voyager_system.domain.medical_center.Pod import *


class Consumer(Account):

    def __init__(self) -> None:
        super().__init__()
        # dispenser-related relations
        self.dispensers = []  # 1-to-n
        self.pods = []  # 1-to-n
        self.dosing_history = []  # 1-to-n
        self.dosing_reminders = []  # 1-to-n

        # personal info
        self.residence = ""
        self.height = -1
        self.weight = -1
        self.gender = -1
        self.units = -1
        self.goal = None

    # add a consumer dosing occurrence when a dosing is performed.
    # * adds a 'dosing record' to dosing_history
    # * changes the current state of the relevant pod(?)
    # returns the new Dosing object.
    # throws AppOperationError if the given pod_id is wrong or does not have the required amount for the dosing.
    def dose(self, pod_serial_number: str, amount: float, time_str, latitude=None, longitude=None):
        is_dosing_possible = self.can_dose(pod_serial_number, amount)
        if not is_dosing_possible:
            raise AppOperationError(
                f"Error: consumer dosing - wrong pod serial number [{pod_serial_number}] or amount [{amount}] ; for consumer [{self.id}]")
        if len(self.dispensers) == 0:
            raise AppOperationError(
                f"Error: consumer dosing - no dispenser to dose with; for consumer [{self.id}]")
        pod: Pod = self.get_pod_by_serial_number(pod_serial_number)
        pod.dose(amount)
        time = parse_string_to_timezone(time_str)
        new_dosing = Dosing(dosing_id=None, pod_serial_number=pod_serial_number,
                            amount=amount, time=time, longitude=longitude, latitude=latitude)
        self.dosing_history.insert(0, new_dosing)
        return new_dosing

    # private helper method. returns boolean!
    def can_dose(self, serial_number, amount: float):
        """checks if a consumer can use a specific pod for dosing

        :param serial_number:
        :param amount:
        :return: True if consumer can dose, else False.
        """
        pod = self.get_pod_by_serial_number(serial_number)
        if pod is None:
            return False
        if pod.remainder < amount or amount <= 0:
            return False
        return True

    # private helper method - returns a pod if the given pod_id is in self.pods
    # else - returns None
    def get_pod_by_serial_number(self, serial_number: str):
        for pod in self.pods:
            if pod.serial_number == serial_number:
                return pod
        return None

    # returns a (SHALLOW) copy of the list of pods registered to the consumer
    def get_pods(self):
        return self.pods.copy()

    # returns a list (SHALLOW COPY) of the dosing in consumer's dosing history which matches the filters
    def get_dosage_history(self, filters=None):
        dosings = [dose for dose in self.dosing_history if self.filter_dosing(dose, filters)]
        return dosings

    # private helper method - returns a True if the dosing and match the given filters
    # else - returns False
    def filter_dosing(self, dosing, filters):
        if filters is None:
            return True
        # @TODO: define the type of filters arg and check filters
        return False

    # receives receives feedback details and dosing-id and adds a new feedback to the dosing
    # returns True if successful, otherwise False.
    # overrides past feedback for the same dosing!
    # throws AppOperationError if the dosing of the given dosing_id is not found in history.
    def provide_feedback(self, dosing_id: int, feedback_rating: int, feedback_comment: str):
        if feedback_rating > 10 or feedback_rating < 1:
            raise AppOperationError(
                f"Error: consumer provide feedback - illegal value for parameter rating - providing feedback for dosing_id [{dosing_id}] for consumer [{self.id}]")
        dosing = self.get_dosing_by_id(dosing_id)
        if dosing is None:
            raise AppOperationError(
                f"Error: consumer provide feedback - wrong dosing_id [{dosing_id}] for consumer [{self.id}]")
        if dosing.feedback is not None:
            raise AppOperationError(
                f"Error: consumer provide feedback - dosing [{dosing_id}] already has feedback provided")
        feedback_time = timezone.now()
        new_feedback = Feedback(id=None, dosing_id=dosing_id, rating=feedback_rating, comment=feedback_comment,
                                time=feedback_time)
        dosing.feedback = new_feedback
        return new_feedback

    # private helper method - returns a past dosing if the given dosing_id is in self.dosing_history
    # else - returns None
    def get_dosing_by_id(self, dosing_id):
        for dose in self.dosing_history:
            if dose.id == dosing_id:
                return dose
        return None

    # registers a new pod to the consumer. receives a podType arg and adds a new pod to the consumer's pod collection.
    # throws AppOperationError if the if a pod with the same id was found.
    def register_pod(self, pod: Pod):
        filtered_pods = [p for p in self.pods if p.serial_number == pod.serial_number]
        if filtered_pods:
            raise AppOperationError(
                f"Error: consumer register pod - pod serial_number [{pod.serial_number}] already registered to consumer [{self.email}]")
        self.pods.insert(0, pod)

    # registers a new dispenser to the consumer. receives a dispenser serial number arg
    # and adds a new dispenser to the consumer's collection.
    # throws AppOperationError if the given serial_number conflicts with an existing dispenser of the consumer.
    def register_dispenser(self, new_dispenser: Dispenser):
        filtered_dispensers = [d for d in self.dispensers if d.serial_number == new_dispenser.serial_number]
        if filtered_dispensers:
            raise AppOperationError(
                f"Error: consumer register dispenser - serial number [{new_dispenser.serial_number}] already exists for consumer [{self.id}]")
        self.dispensers.insert(0, new_dispenser)

    @staticmethod
    def is_valid_dosing_time(time):
        return True

    def get_recommendation(self, stuff):
        raise NotImplementedError("replace this with an actual method")
