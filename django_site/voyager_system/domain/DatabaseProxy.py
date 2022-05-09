from voyager_system.common.ErrorTypes import DataAccessError
from voyager_system.data_access.dtos import *
from voyager_system.domain.medical_center.Consumer import Consumer
from voyager_system.domain.medical_center.Dosing import *
from voyager_system.domain.medical_center.Pod import *
from voyager_system.domain.medical_center.Dispenser import Dispenser
import voyager_system.data_access.database as db
from django.core.exceptions import ObjectDoesNotExist

# TODO:: convert every object returned from DB to Domain Layer object
from voyager_system.domain.system_management.Account import Account


class DatabaseProxy:
    def __init__(self, db_impl, object_cache=None):
        super().__init__()
        # self.db = db_impl
        self.object_cache = object_cache

    # region Account
    def get_account_by_id(self, account_id):
        try:
            dto = db.get_account_by_id(account_id)
            return self.dto_to_account(dto)
        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            err_str = f"Unable to retrieve account from db, with id [{account_id}]." + "\n" + str(e)
            raise DataAccessError(err_str)

    def get_account_by_email(self, email):
        try:
            dto = db.get_account_by_email(email)
            return self.dto_to_account(dto)
        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            err_str = f"Unable to retrieve account from db, with email [{email}]." + "\n" + str(e)
            raise DataAccessError(err_str)

    def add_account(self, email, phone, first_name, last_name, date_of_birth):
        try:
            return db.add_account(email=email, f_name=first_name, l_name=last_name, phone=phone, dob=date_of_birth)
        except Exception as e:
            err_str = f"Unable to add a new account to db, with email [{email}]" + "\n" + str(e)
            raise DataAccessError(err_str)

    def has_account_with_email(self, email):
        return db.has_account_with_email(email)

    def has_account_with_id(self, account_id):
        return db.has_account_with_id(account_id)

    # endregion Account

    # region Consumer
    def get_consumer(self, consumer_id: int):
        try:
            account_dto = db.get_account_by_id(consumer_id)
            consumer_dto = db.get_consumer(consumer_id)
        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            err_str = f"Unable to retrieve consumer from db, with id [{consumer_id}]." + "\n" + str(e)
            raise DataAccessError(err_str)
        consumer = self.dto_to_consumer(consumer_dto, account_dto)
        consumer.pods = self.get_consumer_pods(consumer_id)
        return consumer

    def has_consumer(self, consumer_id):
        return db.has_consumer(consumer_id)

    def add_consumer(self, consumer_id, residence, height, weight, units, gender, goal):
        return db.add_consumer(consumer_id, residence, height, weight, units, gender, goal)

    def update_consumer_personal_info(self, consumer: Consumer):
        # Todo:: make a transaction
        consumer_dto = self.consumer_to_dto(consumer)
        try:
            db.update_consumer(consumer_dto)
        except Exception as e:
            err_str = f"Unable to update consumer [{consumer.id}] in db." + "\n" + str(e)
            raise DataAccessError(err_str)

    def get_consumer_pods(self,consumer_id):
        try:
            pod_dtos = db.get_pods_for_consumer_by_id(consumer_id)
            pods = [self.dto_to_pod(dto) for dto in pod_dtos]
            return pods
        except ObjectDoesNotExist as e:
            return []
        except Exception as e:
            err_str = f"Unable to retrieve consumer's pods from db, with id [{consumer_id}]." + "\n" + str(e)
            raise DataAccessError(err_str)

    # endregion Consumer

    # region Pod
    def add_pod(self, pod: Pod):
        dto = self.pod_to_dto(pod)
        try:
            return db.add_pod(pod_dto=dto)
        except Exception as e:
            err_str = f"Unable to add a new pod to DB, with serial_number [{pod.serial_number}]" + "\n" + str(e)
            raise DataAccessError(err_str)

    def get_pod(self,serial_number: str):
        try:
            pod_dto = db.get_pod_by_serial_number(serial_number)
            return self.dto_to_pod(pod_dto)
        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            err_str = f"Unable to retrieve pod from db, with serial number [{serial_number}]." + "\n" + str(e)
            raise DataAccessError(err_str)

    def update_pod(self, pod: Pod, consumer: Consumer):
        pod_dto = self.pod_to_dto(pod)
        try:
            db.update_pod(pod_dto=pod_dto, consumer_id=consumer.id, pod_type_name=pod.type.name)
        except Exception as e:
            err_str = f"Unable to update pod [{pod.serial_number}] in DB. with consumer [{consumer.id}]." + "\n" + str(e)
            raise DataAccessError(err_str)

    # endregion Pod

    # region PodType
    def add_pod_type(self, pod_type: PodType):
        dto = self.pod_type_to_dto(pod_type)
        try:
            return db.add_pod_type(dto)
        except Exception as e:
            err_str = f"Unable to add a new pod-type [{pod_type.name}] to DB." + "\n" + str(e)
            raise DataAccessError(err_str)

    def update_podtype(self, podtype: PodType):
        dto = self.pod_type_to_dto(podtype)
        try:
            db.update_pod_type(dto)
        except Exception as e:
            err_str = f"Unable to add update pod-type [{podtype.name}]." + "\n" + str(e)
            raise DataAccessError(err_str)

    # endregion PodType

    # region Dispenser
    def add_dispenser(self, dispenser: Dispenser):
        dto = self.dispenser_to_dto(dispenser)
        try:
            return db.add_dispenser(dto)
        except Exception as e:
            err_str = f"Unable to add a new dispenser type to DB, with serial-number [{dispenser.serial_number}]" + "\n" + str(
                e)
            raise DataAccessError(err_str)

    def update_dispenser(self, dispenser: Dispenser, consumer: Consumer):
        dispenser_dto = self.dispenser_to_dto(dispenser)
        try:
            db.update_dispenser(dispenser_dto=dispenser_dto)
        except Exception as e:
            err_str = f"Unable to update dispenser [{dispenser.serial_number}]. with consumer [{consumer.id}]." + "\n" + str(
                e)
            raise DataAccessError(err_str)

    # endregion Dispenser

    # region DTO conversion

    @staticmethod
    def account_to_dto(account: Account):
        dto = AccountDto()
        dto.id = account.id
        dto.email = account.email
        dto.f_name = account.first_name
        dto.l_name = account.last_name
        dto.dob = account.date_of_birth
        # dto.phone = account.phone
        dto.registration_date = account.registration_date
        return dto

    @staticmethod
    def dto_to_account(account_dto: AccountDto):
        account = Account()
        account.id = account_dto.id
        account.email = account_dto.email
        account.first_name = account_dto.f_name
        account.last_name = account_dto.l_name
        account.date_of_birth = account_dto.dob
        # account_dto.phone = dto.phone
        account.registration_date = account_dto.registration_date
        return account

    @staticmethod
    def consumer_to_dto(consumer: Consumer):
        dto = ConsumerDto()
        dto.id = consumer.id
        dto.residence = consumer.residence
        dto.height = consumer.height
        dto.weight = consumer.weight
        dto.gender = consumer.gender
        dto.units = consumer.units
        dto.goal = consumer.goal
        return dto

    @staticmethod
    def dto_to_consumer(consumer_dto: ConsumerDto, account_dto: AccountDto):
        consumer = Consumer()
        # consumer (personal) info
        consumer.residence = consumer_dto.residence
        consumer.height = consumer_dto.height
        consumer.weight = consumer_dto.weight
        consumer.gender = consumer_dto.gender
        consumer.units = consumer_dto.units
        consumer.goal = consumer_dto.goal
        # account info
        consumer.id = account_dto.id
        consumer.email = account_dto.email
        consumer.first_name = account_dto.f_name
        consumer.last_name = account_dto.l_name
        consumer.date_of_birth = account_dto.dob
        consumer.registration_date = account_dto.registration_date
        return consumer

    @staticmethod
    def dispenser_to_dto(dispenser: Dispenser):
        dto = DispenserDto()
        dto.serial_num = dispenser.serial_number
        dto.version = dispenser.version
        dto.registration_date = dispenser.registration_date
        return dto

    @staticmethod
    def dto_to_dispenser(dispenser_dto: DispenserDto):
        disp = Dispenser()
        disp.serial_number = dispenser_dto.serial_num
        disp.version = dispenser_dto.version
        disp.registration_date = dispenser_dto.registration_date
        return disp

    @staticmethod
    def pod_type_to_dto(pod_type: PodType):
        dto = PodTypeDto()
        dto.name = pod_type.name
        dto.substance = pod_type.substance
        # dto.capacity = pod_type.capacity
        dto.company = pod_type.company
        dto.description = pod_type.description
        dto.url = pod_type.url
        return dto

    @staticmethod
    def dto_to_pod_type(podtype_dto: PodTypeDto):
        pod_type = PodType()
        pod_type.name = podtype_dto.name
        pod_type.substance = podtype_dto.substance
        # pod_type.capacity = podtype_dto.capacity
        pod_type.company = podtype_dto.company
        pod_type.url = podtype_dto.url
        # pod_type.url = ""
        pod_type.description = podtype_dto.description
        return pod_type

    @staticmethod
    def pod_to_dto(pod: Pod):
        dto = PodDto
        dto.serial_num = pod.serial_number
        dto.pod_type = DatabaseProxy.pod_type_to_dto(pod.type)
        dto.remainder = pod.remainder
        return dto

    @staticmethod
    def dto_to_pod(pod_dto: PodDto):
        pod: Pod = Pod()
        pod.serial_number = pod_dto.serial_num
        pod.type = DatabaseProxy.dto_to_pod_type(pod_dto.pod_type)
        pod.remainder = pod_dto.remainder
        return pod

    def dosing_to_dto(self, dosing: Dosing):
        raise NotImplementedError("method not implemented yet")

    def dosing_reminder_to_dto(self, reminder: DosingReminder):
        raise NotImplementedError("method not implemented yet")

    # endregion DTO conversion


    def add_company(self, business_name: str):
        db.add_company(business_name)
