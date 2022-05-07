from voyager_system.common.ErrorTypes import DataAccessError
from voyager_system.domain.medical_center.Dispenser import Dispenser
import voyager_system.data_access.database as db


# TODO:: convert every object returned from DB to Domain Layer object
class DatabaseProxy:
    def __init__(self, db_impl, object_cache=None):
        super().__init__()
        # self.db = db_impl
        self.object_cache = object_cache

    # region Account
    def get_account_by_id(self, account_id):
        try:
            return db.get_account_by_id(account_id)
        except Exception as e:
            err_str = e.__str__()
            raise DataAccessError(f"Unable to retrieve account from db, with id {account_id}." + "\n" + err_str)

    def get_account_by_email(self, email):
        return db.get_account_by_email(email)

    def add_account(self, email, phone, first_name, last_name, date_of_birth):
        try:
            return db.add_account(email=email, f_name=first_name, l_name=last_name, phone=phone, dob=date_of_birth)
        except Exception as e:
            err_str = e.__str__()
            raise DataAccessError(f"Unable to add a new account to db, with email {email}" + "\n" + err_str)

    def has_account_with_email(self, email):
        return db.has_account_with_email(email)

    def has_account_with_id(self, account_id):
        return db.has_account_with_id(account_id)

    # endregion Account

    # region Consumer
    def get_consumer_by_id(self, consumer_id):
        return db.get_consumer(consumer_id)

    def has_consumer(self, consumer_id):
        return db.has_consumer(consumer_id)

    def add_consumer(self, consumer_id, residence, height, weight, units, gender, goal):
        return db.add_consumer(consumer_id, residence, height, weight, units, gender, goal)

    def update_consumer(self, consumer):
        pass

    def consumer_register_dispenser(self, consumer_id, dispenser_serial_number):
        return db.set_dispenser_consumer(dispenser_serial_number, consumer_id)
        # dto = self.get_dispenser_dto(dispenser_serial_number)
        # return db.update_dispenser(dto)

    # endregion Consumer

    # region DTO conversion

    def get_dispenser_dto(self, dispenser: Dispenser):
        raise NotImplementedError("method not implemented yet")

    # endregion DTO conversion
