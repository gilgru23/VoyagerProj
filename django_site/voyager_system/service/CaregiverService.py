from voyager_system.common import Result
from voyager_system.common.ErrorTypes import AppOperationError, DataAccessError

from voyager_system.domain.medical_center.MedicalCenter import MedicalCenter


class ConsumerService:
    def __init__(self, med_center: MedicalCenter) -> None:
        self.med_center: MedicalCenter = med_center
        pass

    def associate_to_consumer(self, caregiver_id:int, consumer_id: int):
        try:
            raise NotImplementedError("do this")
            return Result.success()
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")

    def get_consumers_dosing_history(self, caregiver_id:int):
        try:
            raise NotImplementedError("do this")
            return Result.success(history)
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")


