from domain.User import User
from domain.medicalCenter.Dosing import Dosing

from datetime import datetime
from random import randint

class Consumer(User):

    def __init__(self) -> None:
        # dispenser-related relations
        self.dispenser = None       # 1-to-1 (?)
        self.pods = []              # 1-to-n
        self.dosing_history = []    # 1-to-n

        # personal info
        self.residence = ""
        self.height = None
        self.weight = None
        self.gender = ""
        self.goal = ""
        pass

    # add a consumer dosing occurrence when a dosing is performed.
    # - adds a 'dosing record' to dosing_history
    # - changes the current state of the relevant pod(?)
    async def dose(self,pod_id, pod_type, amount: float, location):
        if not self.can_dose(pod_id,pod_type,amount):
            return False
        # @TODO: replace datetime.now with a more generic time method
        dosing_time = datetime.now()
        # @TODO: replace random.randint with an ORM generated id (when adding DAL)
        dosing_id = randint(1, 1000)
        new_dosing = Dosing(pod_id=pod_id, dosing_id=dosing_id, time= dosing_time, location=location)
        # @TODO: add a call (await) to IMapper (when adding DAL)
        self.dosing_history.insert(0, new_dosing)
        return True

    # checks if a consumer can use a specific pod for dosing
    def can_dose(self, pod_id, amount: float):
        pod = self.get_pod_by_id(pod_id)
        if (pod is None) or (pod.remainder < amount):
            return False
        return True

    # private helper method - returns a pod if the given pod_id is in self.pods
    # else - returns None
    def get_pod_by_id(self, pod_id):
        for pod in self.pods:
            if pod.id == pod_id:
                return pod
        return None

    # returns a list of the dosing in consumer's dosing history which matches the filters
    def get_dosage_history(self, filters=None):
        dosings = [dos for dos in self.dosing_history if self.filter_dosing(dos,filters)]
        return dosings

    # private helper method - returns a True if the dosing and match the given filters
    # else - returns False
    def filter_dosing(self, dosing, filters):
        if filters is None:
            return True
        # @TODO: define the type of filters arg and check filters
        return False

    async def provide_feedback(self, dosing, feedback):
        raise NotImplementedError("replace this with an actual method")

    async def get_recommendation(self, stuff):
        raise NotImplementedError("replace this with an actual method")