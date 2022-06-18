from django.utils import timezone

from voyager_system.common.ErrorTypes import AppOperationError
from voyager_system.data_access.DatabaseProxy import DatabaseProxy
from voyager_system.domain.medical_center.Dispenser import Dispenser
from voyager_system.domain.medical_center.Pod import Pod, PodType


class MarketPlace:
    def __init__(self, db_proxy: DatabaseProxy) -> None:
        self.db = db_proxy

    def validate_pod(self, serial_num: str, pod_type_name: str) -> Pod:
        pod = self.db.get_pod(serial_num)
        if (pod is None) or (pod.type_name != pod_type_name):
            err_str = f'Invalid pod serial number [{serial_num}] or type [{pod_type_name}]'
            # log err_str
            raise AppOperationError(err_str)
        return pod

    def create_pod(self, serial_num: str, pod_type_name: str):
        pod_type = self.get_pod_type_from_typeId(pod_type_name)
        pod = Pod.from_type(serial_number=serial_num, pod_type=pod_type)
        self.db.add_pod(pod)

    def get_pod_type_from_typeId(self, pod_type_name: str) -> PodType:
        return PodType(name=pod_type_name, substance="Nothing", description="even less")

    def validate_dispenser(self, serial_num: str, version: str, consumer_id: int) -> Dispenser:
        disp, owner_id = self.db.get_dispenser(serial_num)
        if (disp is None) or (disp.version != version):
            err_str = f'Invalid dispenser serial number [{serial_num}] or version [{version}]'
            # log err_str
            raise AppOperationError(err_str)
        if (owner_id is not None) and (owner_id != consumer_id):
            err_str = f'Invalid dispenser serial number [{serial_num}]: the dispenser is already registered to a different consumer'
            # log err_str
            raise AppOperationError(err_str)

        disp.registration_date = timezone.now()
        return disp

    def create_dispenser(self, serial_num: str, version: str):
        disp = Dispenser()
        disp.serial_number = serial_num
        disp.version = version
        disp.registration_date = timezone.now()
        self.db.add_dispenser(dispenser=disp)
