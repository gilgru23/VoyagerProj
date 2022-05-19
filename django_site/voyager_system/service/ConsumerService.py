from voyager_system.common import Result
from voyager_system.common.ErrorTypes import AppOperationError, DataAccessError

from voyager_system.domain.medical_center.MedicalCenter import MedicalCenter


class ConsumerService:
    def __init__(self, med_center: MedicalCenter) -> None:
        self.med_center: MedicalCenter = med_center
        pass

    def update_personal_info(self, consumer_id: int, residence: str, height: int,
                             weight: int, units, gender, goal: any):
        pass

    def register_dispenser_to_consumer(self, consumer_id: int, dispenser_serial_num: str, dispenser_version: str):
        try:
            self.med_center.consumer_register_dispenser(consumer_id, dispenser_serial_num,dispenser_version)
            return Result.success()
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")

    def register_pod_to_consumer(self, consumer_id: int, pod_serial_num: str, pod_type: str):
        try:
            self.med_center.consumer_register_pod(consumer_id=consumer_id,
                                                  pod_serial_num=pod_serial_num,
                                                  pod_type_name=pod_type)
            return Result.success()
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")

    def get_consumer_pods(self, consumer_id):
        try:
            pods = self.med_center.get_consumer_pods(consumer_id=consumer_id)
            return Result.success(pods)
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")

    def get_consumer_dosing_history(self, consumer_id):
        try:
            history = self.med_center.get_consumer_dosing_history(consumer_id=consumer_id)
            return Result.success(history)
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")

    def consumer_dose(self, consumer_id, pod_serial_num: str, amount: float, time, latitude=None, longitude=None):
        try:
            self.med_center.consumer_dose(consumer_id, pod_serial_num, amount, time, latitude, longitude)
            return Result.success()
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")


# - set_dosing_reminder
# - get_recomendation(consumer_id)
# - set_regimen(consumer_id)
# - get_regimen(consumer_id)

