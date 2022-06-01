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

    def get_consumer_dispensers(self, consumer_id):
        try:
            pods = self.med_center.get_consumer_dispensers(consumer_id=consumer_id)
            return Result.success(pods)
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

    def consumer_dose(self, consumer_id, pod_serial_num: str, amount: float, time, latitude=-1.0, longitude=-1.0):
        try:
            self.med_center.consumer_dose(consumer_id, pod_serial_num, amount, time, latitude, longitude)
            return Result.success()
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")

    def provide_feedback_to_dosing(self, consumer_id, dosing_id: int, rating: int, comment: str,):
        try:
            self.med_center.consumer_provide_feedback(consumer_id,dosing_id,rating,comment)
            return Result.success()
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")

    def get_feedback_for_dosing(self, consumer_id, dosing_id):
        try:
            feedback = self.med_center.get_feedback_for_dosing(consumer_id=consumer_id, dosing_id=dosing_id)
            return Result.success(feedback)
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")

# - set_dosing_reminder
# - get_recomendation(consumer_id)
# - set_regimen(consumer_id)
# - get_regimen(consumer_id)

