

# from voyager_system.domain.medicalCenter.MedicalCenter import MedicalCenter
import voyager_system.domain.medicalCenter.MedicalCenter as med_cen

def register_dispenser(consumer_id: int, dispenser_serial_num: str):
    med_cen.consumer_register_dispenser(consumer_id, dispenser_serial_num)

# class ConsumerService:
#     def __init__(self) -> None:
#         pass

#     async def define_goals(self, user_id: int, goals) -> str:
#         pass

#     async def update_personal_info(self, user_id: int, info):
#         pass

#     async def register_dispenser(self, dispenser_id: str):
#         pass
