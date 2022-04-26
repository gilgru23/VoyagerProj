

from voyager_system.domain.medicalCenter.MedicalCenter import MedicalCenter
# import voyager_system.domain.medicalCenter.MedicalCenter


class ConsumerService:
    def __init__(self, med_center: MedicalCenter) -> None:
        self.med_center = med_center
        pass

    def register_dispenser(self, consumer_id: int, dispenser_serial_num: str):
        self.med_center.consumer_register_dispenser(consumer_id, dispenser_serial_num)

    async def update_personal_info(self, user_id: int, info):
        pass

    async def define_goals(self, user_id: int, goals) -> str:
        pass

