from domain.User import User


class Consumer(User):

    # dispenser-related relations
    dispenser = None        # 1-to-1 (?)
    pods = None             # 1-to-n
    dosing_history = None   # 1-to-n

    # personal info
    residence = ""
    height = None
    weight = None
    gender = ""
    goal = ""



    def __init__(self) -> None:
        pass

    async def dose(self, pod_type, ammount: float):
        raise NotImplementedError("replace this with an actual method")

    async def get_dosage_history(self, filters=None):
        raise NotImplementedError("replace this with an actual method")

    async def provide_feedback(self, dosing, feedback):
        raise NotImplementedError("replace this with an actual method")

    async def get_recommendation(self, stuff):
        raise NotImplementedError("replace this with an actual method")