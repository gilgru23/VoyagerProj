
from datetime import datetime
from random import randint

from voyager_system.data_access.dtos import ConsumerDto
from voyager_system.domain.system_management.Account import Account
from voyager_system.common.ErrorTypes import AppOperationError
from voyager_system.domain.medical_center.Dispenser import Dispenser
from voyager_system.domain.medical_center.Dosing import *
from voyager_system.domain.medical_center.Pod import *


class Consumer(Account):

    def __init__(self) -> None:
        super().__init__()
        # dispenser-related relations
        self.dispensers = []                    # 1-to-n (?)
        self.pods = []                          # 1-to-n
        self.dosing_history = []                # 1-to-n
        self.dosing_reminders = []                     # 1-to-n

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
    # returns True if successful, otherwise False.
    # throws AppOperationError if the given pod_id is wrong or does not have the required amount for the dosing.
    async def dose(self,pod_id, amount: float, location):
        is_dosing = await self.can_dose(pod_id,amount)
        if not is_dosing:
            raise AppOperationError(f"Error: consumer dosing - wrong pod_id [{pod_id}] or amount [{amount}] for consumer [{self.id}]")
        pod = await self.get_pod_by_id(pod_id)
        pod.dose(amount)
        # @TODO: replace datetime.now with a more generic time method
        dosing_time = datetime.now()
        # @TODO: replace random.randint with an ORM generated id (when adding DAL)
        dosing_id = randint(1, 100000)
        new_dosing = Dosing(dosing_id=dosing_id, pod_id=pod_id, pod_type_id= pod.type.type_id, amount=amount, time=dosing_time, location=location)
        self.dosing_history.insert(0, new_dosing)

    # private helper method. returns boolean!
    async def can_dose(self, pod_id, amount: float):
        """checks if a consumer can use a specific pod for dosing

        :param pod_id:
        :param amount:
        :return: True if consumer can dose, else False.
        """
        pod = await self.get_pod_by_id(pod_id)
        if pod is None:
            return False
        if pod.remainder < amount or amount <= 0:
            return False
        return True

    # private helper method - returns a pod if the given pod_id is in self.pods
    # else - returns None
    async def get_pod_by_id(self, pod_id):
        for pod in self.pods:
            if pod.id == pod_id:
                return pod
        return None

    # returns a (SHALLOW) copy of the list of pods registered to the consumer
    async def get_pods(self):
        return self.pods.copy()

    # returns a list (SHALLOW COPY) of the dosing in consumer's dosing history which matches the filters
    async def get_dosage_history(self, filters=None):
        dosings = [dose for dose in self.dosing_history if self.filter_dosing(dose,filters)]
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
    async def provide_feedback(self, dosing_id, feedback_rating, feedback_description):
        dosing = await self.get_dosing_by_id(dosing_id)
        if dosing is None:
            raise AppOperationError(f"Error: consumer provide feedback - wrong dosing_id [{dosing_id}] for consumer [{self.id}]")
        # @TODO: replace datetime.now with a more generic time method
        feedback_time = datetime.now()
        # @TODO: replace random.randint with an ORM generated id (when adding DAL)
        feedback_id = randint(1, 100000)
        new_feedback = Feedback(id=feedback_id,rating=feedback_rating,description=feedback_description,time=feedback_time)
        dosing.feedback = new_feedback

    # private helper method - returns a past dosing if the given dosing_id is in self.dosing_history
    # else - returns None
    async def get_dosing_by_id(self, dosing_id):
        for dose in self.dosing_history:
            if dose.id == dosing_id:
                return dose
        return None

    # registers a new pod to the consumer. receives a podType arg and adds a new pod to the consumer's pod collection.
    # throws AppOperationError if the if a pod with the same id was found.
    def register_pod(self,pod: Pod):
        filtered_pods = [p for p in self.pods if p.serial_number == pod.serial_number]
        if filtered_pods:
            raise AppOperationError(f"Error: consumer register pod - pod serial_number [{pod.serial_number}] already registered to consumer [{self.id}]")
        self.pods.insert(0, pod)

    # registers a new dispenser to the consumer. receives a dispenser serial number arg
    # and adds a new dispenser to the consumer's collection.
    # throws AppOperationError if the given serial_number conflicts with an existing dispenser of the consumer.
    async def register_dispenser(self, serial_number):
        filtered_dispensers = [disp for disp in self.dispensers if disp.serial == serial_number]
        if filtered_dispensers:
            raise AppOperationError(f"Error: consumer register dispenser - serial number [{serial_number}] already exists for consumer [{self.id}]")
        # @TODO: replace datetime.now with a more generic time method
        registration_time = datetime.now()
        new_dispenser = Dispenser(serial_number=serial_number,registration_time=registration_time)
        self.dispensers.insert(0, new_dispenser)

    async def get_recommendation(self, stuff):
        raise NotImplementedError("replace this with an actual method")
