from voyager_system.common import Result
from voyager_system.common.ErrorTypes import AppOperationError, DataAccessError

from voyager_system.domain.medical_center.MedicalCenter import MedicalCenter


class ConsumerService:
    def __init__(self, med_center: MedicalCenter) -> None:
        self.med_center = med_center
        pass

    def update_personal_info(self, consumer_id: int, residence: str, height: int,
                             weight: int, units, gender, goal: any):
        pass

    def register_dispenser_to_consumer(self, consumer_id: int, dispenser_serial_num: str):
        try:
            self.med_center.consumer_register_dispenser(consumer_id, dispenser_serial_num)
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
        return Result.failure("not working yet")
        # try:
        #     pods = self.med_center.get_consumer_pods(consumer_id=consumer_id)
        #     return Result.success(pods)
        # except AppOperationError as e:
        #     return Result.failure(str(e))
        # except DataAccessError as e:
        #     return Result.failure("Unable to complete the operation")


# - dose(consumer_id, pod, amount, units)
# - set_dosing_reminder
# - get_recomendation(consumer_id)
# - set_regimen(consumer_id)
# - get_regimen(consumer_id)

