from voyager_system.common import Result

from voyager_system.domain.medical_center.MedicalCenter import MedicalCenter


class ConsumerService:
    def __init__(self, med_center: MedicalCenter) -> None:
        self.med_center = med_center
        pass

    def update_personal_info(self, consumer_id: int, residence: str, height: int,
                             weight: int, units, gender, goal: any):
        pass

    def register_dispenser_to_consumer(self, consumer_id: int, dispenser_serial_num: str):
        self.med_center.consumer_register_dispenser(consumer_id, dispenser_serial_num)

    def register_pod_to_consumer(self, consumer_id: int, pod_serial_num: str, pod_type: str):
        self.med_center.consumer_register_pod(consumer_id=consumer_id,
                                              pod_serial_num=pod_serial_num,
                                              pod_type_name=pod_type)

# - dose(consumer_id, pod, amount, units)
# - get_consumers_pods(consumer_id)
# - set_dosing_reminder
# - get_recomendation(consumer_id)
# - set_regimen(consumer_id)
# - get_regimen(consumer_id)

