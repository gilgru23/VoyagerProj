from voyager_system.domain.DatabaseProxy import DatabaseProxy
from voyager_system.data_access import database as db
from voyager_system.domain.marketplace.MarketPlace import MarketPlace

from voyager_system.domain.system_management.SystemManagement import SystemManagement
from voyager_system.domain.medical_center.MedicalCenter import MedicalCenter
from voyager_system.service.ConsumerService import ConsumerService
from voyager_system.service.GuestService import GuestService

db_proxy = DatabaseProxy(db_impl=db)
marketplace = MarketPlace(db_proxy=db_proxy)
medical_center = MedicalCenter(db_proxy=db_proxy, marketplace=marketplace)
system_management = SystemManagement(medical_center=medical_center,db_proxy=db_proxy)
consumer_service = ConsumerService(med_center=medical_center)
guest_service = GuestService(sys_management=system_management)


def get_consumer_service():
    return consumer_service


def get_guest_service():
    return guest_service


def get_db_proxy():
    return db_proxy

