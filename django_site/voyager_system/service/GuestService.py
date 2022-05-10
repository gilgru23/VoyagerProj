
from voyager_system.common import Result
from voyager_system.domain.system_management.SystemManagement import SystemManagement
from voyager_system.common.ErrorTypes import AppOperationError, DataAccessError


class GuestService:
    def __init__(self, sys_management: SystemManagement) -> None:
        self.system_management = sys_management


    def create_account(self, email: str, phone: str, f_name: str, l_name: str, dob: str):
        try:
            self.system_management.create_account(email, phone, f_name, l_name, dob)
            return Result.success()
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")


    def create_consumer_profile(self, consumer_id: int, residence: str, height: int, weight: int, units, gender,
                                goal: any):
        try:
            self.system_management.create_consumer_profile(consumer_id, residence, height, weight, units, gender, goal)
            return Result.success()
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")


    def get_account_details(self, account_id: int):
        try:
            account_details = self.system_management.get_account_details(account_id)
            return Result.success(account_details)
        except AppOperationError as e:
            return Result.failure(str(e))
        except DataAccessError as e:
            return Result.failure("Unable to complete the operation")



    def get_consumer_profile(self, consumer_id: int):
        return {'residence:':"here",'height:':"180",'weight':"75",'units':1}
