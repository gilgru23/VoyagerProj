
from voyager_system.common import Result
from voyager_system.domain.system_management.SystemManagement import SystemManagement
from voyager_system.common.ErrorTypes import AppOperationError, DataAccessError


class GuestService:
    def __init__(self, sys_management: SystemManagement) -> None:
        self.system_management = sys_management


    def create_account(self, email: str, phone: str, f_name: str, l_name: str, dob: str) -> str:
        try:
            self.system_management.create_account(email, phone, f_name, l_name, dob)
            return Result.success()
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")


    def create_consumer_profile(self, consumer_id: int, residence: str, height: int, weight: int, units, gender,
                                goal: any) -> str:
        try:
            self.system_management.create_consumer_profile(consumer_id, residence, height, weight, units, gender, goal)
            return Result.success()
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")
