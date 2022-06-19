from voyager_system.common import Result
from voyager_system.common.ErrorTypes import *
from voyager_system.domain.marketplace.MarketPlace import MarketPlace


class ManagerService:
    def __init__(self, marketplace: MarketPlace) -> None:
        self.marketplace = marketplace

    def add_dispenser(self, new_serial_number, dispenser_version) -> str:
        return self.manage_request_calls(
            lambda: self.marketplace.add_dispenser(serial_num=new_serial_number, version=dispenser_version))

    def add_pod(self, new_serial_number, pod_type: str) -> str:
        return self.manage_request_calls(
            lambda: self.marketplace.add_pod(serial_num=new_serial_number, pod_type=pod_type))

    def get_approval_requests(self) -> str:
        pass


    @staticmethod
    def manage_request_calls(func):
        REQ_TIMEOUT = 20
        for c in range(REQ_TIMEOUT):
            try:
                output = func()
                return Result.success(output)
            except ConcurrentUpdateError as e:
                pass
            except AppOperationError as e:
                return Result.failure(str(e))
            except DataAccessError as e:
                return Result.failure("Unable to complete the operation in DB")
        return Result.failure(f"Unable to complete the operation")
