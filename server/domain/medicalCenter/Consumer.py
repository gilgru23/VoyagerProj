
from datetime import datetime
from random import randint


import domain.common.Result as Res
from domain.User import User
from domain.medicalCenter.Dispenser import Dispenser
from domain.medicalCenter.Dosing import *
from domain.medicalCenter.Pod import *


class Consumer(User):

    def __init__(self) -> None:
        super().__init__()
        # dispenser-related relations
        self.dispensers = []                    # 1-to-n (?)
        self.pods = []                          # 1-to-n
        self.dosing_history = []                # 1-to-n

        # personal info
        self.residence = ""
        self.height = None
        self.weight = None
        self.gender = ""
        self.goal = ""

    # add a consumer dosing occurrence when a dosing is performed.
    # * adds a 'dosing record' to dosing_history
    # * changes the current state of the relevant pod(?)
    # returns True if successful, otherwise False.
    # @TODO: make method async ?? (possibly can be avoided, for every mention in this file,
    # @TODO: if we confine DB operations to Medical-Center class)
    async def dose(self,pod_id, amount: float, location):
        is_dosing = await self.can_dose(pod_id,amount)
        if not is_dosing:
            return Res.failure(f"Error: consumer dosing - wrong pod_id [{pod_id}] for consumer [{self.id}]")
        pod_res = await self.get_pod_by_id(pod_id)
        pod = Res.get_value(pod_res)
        pod.dose(amount)
        # @TODO: replace datetime.now with a more generic time method
        dosing_time = datetime.now()
        # @TODO: replace random.randint with an ORM generated id (when adding DAL)
        dosing_id = randint(1, 100000)
        new_dosing = Dosing(pod_id=pod_id, dosing_id=dosing_id,amount=amount, time=dosing_time, location=location)
        self.dosing_history.insert(0, new_dosing)
        return Res.success()

    # private helper method. returns boolean!
    # checks if a consumer can use a specific pod for dosing
    async def can_dose(self, pod_id, amount: float):
        pod_res = await self.get_pod_by_id(pod_id)
        if Res.is_failure(pod_res):
            return False
        pod = Res.get_value(pod_res)
        if pod.remainder < amount:
            return False
        return True

    # private helper method - returns a pod if the given pod_id is in self.pods
    # else - returns None
    async def get_pod_by_id(self, pod_id):
        for pod in self.pods:
            if pod.id == pod_id:
                return Res.success(pod)
        return Res.failure(f"Error: get pod - wrong pod_id [{pod_id}] for consumer [{self.id}]")

    # returns a (SHALLOW) copy of the list of pods registered to the consumer
    async def get_pods(self):
        return Res.success(self.pods.copy())

    # returns a list (SHALLOW COPY) of the dosing in consumer's dosing history which matches the filters
    async def get_dosage_history(self, filters=None):
        dosings = [dose for dose in self.dosing_history if self.filter_dosing(dose,filters)]
        return Res.success(dosings)

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
    async def provide_feedback(self, dosing_id, feedback_rating, feedback_description):
        dosing = await self.get_dosing_by_id(dosing_id)
        if dosing is None:
            return Res.failure(f"Error: consumer provide feedback - wrong dosing_id [{dosing_id}] for consumer [{self.id}]")
        # @TODO: replace datetime.now with a more generic time method
        feedback_time = datetime.now()
        # @TODO: replace random.randint with an ORM generated id (when adding DAL)
        feedback_id = randint(1, 100000)
        new_feedback = Feedback(id=feedback_id,rating=feedback_rating,description=feedback_description,time=feedback_time)
        dosing.feedback = new_feedback
        return Res.success()

    # private helper method - returns a past dosing if the given dosing_id is in self.dosing_history
    # else - returns None
    async def get_dosing_by_id(self, dosing_id):
        for dose in self.dosing_history:
            if dose.id == dosing_id:
                return dose
        return None

    # registers a new pod to the consumer. receives a podType arg and adds a new pod to the consumer's pod collection.
    async def register_pod(self, pod_type: PodType):
        # @TODO: replace ID with an ORM generated id (when adding DAL)
        if self.pods:
            id = 1 + max(pod.id for pod in self.pods)
        else:
            id = 1
        new_pod = Pod(pod_id=id, pod_type=pod_type)
        self.pods.insert(0, new_pod)
        return Res.success()

    # registers a new dispenser to the consumer. receives a dispenser serial number arg
    # and adds a new dispenser to the consumer's collection.
    async def register_dispenser(self, serial_number):
        # # @TODO: replace ID with an ORM generated id (when adding DAL)
        new_dispenser = Dispenser(serial_number=serial_number)
        self.dispensers.insert(0, new_dispenser)
        return Res.success()

    async def get_recommendation(self, stuff):
        raise NotImplementedError("replace this with an actual method")

