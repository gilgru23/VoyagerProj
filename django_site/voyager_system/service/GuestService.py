# import voyager_system.domain.SystemManagement as SystemManagement

from voyager_system.domain.SystemManagement import SystemManagement


class GuestService:
    def __init__(self, sys_management: SystemManagement) -> None:
        self.system_management = sys_management

    # email, pwd, phone, f_name, l_name, dob
    def create_account(self, email: str, phone: str, f_name: str, l_name: str, dob: str) -> str:
        return self.system_management.create_account(email, phone, f_name, l_name, dob)

    # def login(email: str, pwd: str) -> str:
    #     return SystemManagement.login(email, pwd)
    def create_consumer_profile(self, id: int, residence: str, height: int, weight: int, units: str, gender: chr,
                                goal: any) -> str:
        return self.system_management.create_consumer_profile(id, residence, height, weight, units, gender, goal)
