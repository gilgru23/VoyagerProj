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


    def register_pod_to_consumer(self, consumer_id: int, pod_id: int, pod_type: str):
        self.med_center.consumer_register_dispenser(self, consumer_id, pod_id, pod_type)


# - dose
# - get consumer's pods
# - set dosing reminder
