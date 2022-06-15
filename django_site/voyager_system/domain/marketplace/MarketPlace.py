from django.utils import timezone

from voyager_system.data_access.DatabaseProxy import DatabaseProxy
from voyager_system.domain.medical_center.Dispenser import Dispenser
from voyager_system.domain.medical_center.Pod import Pod, PodType


class MarketPlace:
    def __init__(self, db_proxy: DatabaseProxy) -> None:
        self.db = db_proxy



    def validate_pod(self, serial_num: str, pod_type_name: str) -> Pod:
        pod_type = self.get_pod_type_from_typeId(pod_type_name)
        pod = Pod.from_type(serial_number=serial_num, pod_type=pod_type)
        return pod

    def get_pod_type_from_typeId(self, pod_type_name: str) -> PodType:
        return PodType(name=pod_type_name, substance="Nothing", description="even less")


    def validate_dispenser(self, serial_num: str, version: str) -> Dispenser:
        disp = Dispenser()
        disp.serial_number = serial_num
        disp.version = version
        disp.registration_date = timezone.now()
        return disp
