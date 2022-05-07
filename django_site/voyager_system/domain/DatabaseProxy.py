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
            # return self.dto_to_account(dto)
            return dto
        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            err_str = f"Unable to retrieve account from db, with id [{account_id}]." + "\n" + str(e)
            raise DataAccessError(err_str)

    def get_account_by_email(self, email):
        try:
            dto = db.get_account_by_email(email)
            # return self.dto_to_account(dto)
            return dto
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
            dto = db.get_consumer(consumer_id)
            # return self.dto_to_consumer(dto)
            return dto
        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            err_str = f"Unable to retrieve consumer from db, with id [{consumer_id}]." + "\n" + str(e)
            raise DataAccessError(err_str)

    def has_consumer(self, consumer_id):
        return db.has_consumer(consumer_id)

    def add_consumer(self, consumer_id, residence, height, weight, units, gender, goal):
        # Todo:: make a transaction
        return db.add_consumer(consumer_id, residence, height, weight, units, gender, goal)

    def update_consumer(self, consumer: Consumer):
        consumer_dto = self.consumer_to_dto(consumer)
        # pod_dots = [self.pod_to_dto(p) for p in consumer.pods]
        # dispenser_dots = [self.dispenser_to_dto(d) for d in consumer.dispensers]
        # dosing_dots = [self.dosing_to_dto(d) for d in consumer.dosing_history]
        # reminders_dots = [self.dosing_reminder_to_dto(r) for r in consumer.dosing_reminders]

        pass

    def consumer_add_pod(self, consumer: Consumer, pod: Pod):
        pod_dto = self.pod_to_dto(pod)
        try:
            db.update_pod(pod_dto=pod_dto, consumer_id=consumer.id)
        except Exception as e:
            err_str = f"Unable to add a pod [{pod.id}] to consumer [{consumer.id}]." + "\n" + str(e)
            raise DataAccessError(err_str)

    def consumer_update_pod(self, consumer: Consumer, pod: Pod):
        pod_dto = self.pod_to_dto(pod)
        try:
            db.update_pod(pod_dto=pod_dto, consumer_id=consumer.id)
        except Exception as e:
            err_str = f"Unable to add a pod [{pod.id}] to consumer [{consumer.id}]." + "\n" + str(e)
            raise DataAccessError(err_str)

    def consumer_add_dispenser(self, consumer: Consumer, dispenser: Dispenser):
        disp_dto = self.dispenser_to_dto(dispenser)
        try:
            db.update_dispenser(dispenser_dto=disp_dto, consumer_id=consumer.id)
        except Exception as e:
            err_str = f"Unable to add a pod [{dispenser.serial_number}] to consumer [{consumer.id}]." + "\n" + str(e)
            raise DataAccessError(err_str)
        # return db.set_dispenser_consumer(dispenser_serial_number, consumer_id)
        # dto = self.get_dispenser_dto(dispenser_serial_number)
        # return db.update_dispenser(dto)

    # endregion Consumer

    # region DTO conversion

    def account_to_dto(self, account: Account):
        dto = AccountDto()
        dto.id = account.id
        dto.email = account.email
        dto.f_name = account.first_name
        dto.l_name = account.last_name
        dto.dob = account.date_of_birth
        dto.registration_date = account.registration_date
        return dto

    def dto_to_account(self, account_dto: AccountDto):
        account = Account()
        account.id = account_dto.id
        account.email = account_dto.email
        account.f_name = account_dto.f_name
        account.l_name = account_dto.l_name
        account.dob = account_dto.dob
        account.registration_date = account_dto.registration_date
        return account

    def consumer_to_dto(self, consumer: Consumer):
        dto = ConsumerDto()
        dto.residence = consumer.residence
        dto.height = consumer.height
        dto.weight = consumer.weight
        dto.gender = consumer.gender
        # dto.units = consumer.units
        dto.goal = consumer.goal
        return dto

    def dto_to_consumer(self, consumer_dto: ConsumerDto):
        consumer = Consumer()
        consumer.residence = consumer_dto.residence
        consumer.height = consumer_dto.height
        consumer.weight = consumer_dto.weight
        consumer.gender = consumer_dto.gender
        # consumer.units = consumer_dto.units
        consumer.goal = consumer_dto.goal
        return consumer


    def dispenser_to_dto(self, dispenser: Dispenser):
        raise NotImplementedError("method not implemented yet")

    def pod_to_dto(self, pod: Pod):
        raise NotImplementedError("method not implemented yet")

    def dosing_to_dto(self, dosing: Dosing):
        raise NotImplementedError("method not implemented yet")

    def dosing_reminder_to_dto(self, reminder: DosingReminder):
        raise NotImplementedError("method not implemented yet")

    # endregion DTO conversion
