import re
from voyager_system.common.ErrorTypes import AppOperationError
from voyager_system.common.DateTimeFormats import date_to_str
from voyager_system.domain.medical_center.MedicalCenter import MedicalCenter
from voyager_system.data_access.DatabaseProxy import DatabaseProxy


# @TODO:: add logs
from voyager_system.domain.system_management.Account import Account


class SystemManagement:

    def __init__(self, medical_center: MedicalCenter, db_proxy: DatabaseProxy) -> None:
        self.med_center: MedicalCenter = medical_center
        self.db_proxy: DatabaseProxy = db_proxy



    EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    # todo: handle phone number
    def create_account(self, email, phone, f_name, l_name, dob) -> str:
        """
        creates a new account in the system

        :param email: string - valid email address
        :param phone: string - user's phone number
        :param f_name: string - user's first name
        :param l_name: string - user's last name
        :param dob: string - user's date of birth. format - YYYY-MM-DD
        :return: None
        :raise AppOperationError: throws if any of the following occur:
                1. there already exist an account with the same id
                2. any of the parameters is invalid
        :raise DataAccessError: throws if db operation fails
        """
        if not re.search(self.EMAIL_REGEX, email):
            raise AppOperationError(f"Invalid parameters")
        if not (email and phone and f_name and l_name and dob):
            raise AppOperationError(f"Invalid parameters")
        if self.is_email_registered(email):
            #  log f"There already exits an account with email: [{email}]"
            raise AppOperationError(f"There already exits an account with email: [{email}]")
        # Todo: add Registration-Date as an arg to db
        self.db_proxy.add_account(email, phone, f_name, l_name, dob)


    def create_consumer_profile(self, consumer_id: int, residence: str, height: int, weight: int,
                                units, gender, goal: any):
        """
        creates a new Consumer profile for an Account in the system

        :param consumer_id: int - id of the account
        :param residence: string - text describing consumer's place of residence
        :param height: int - height of the consumer
        :param weight: int - weight of the consumer
        :param units: int - the units of the measurements (enum)
        :param gender: int - consumer's gender (enum)
        :param goal: string - consumer goals for using the system
        :return: None
        :raise AppOperationError: throws if any of the following occur:
                1. an account with the same id doesnt exit
                2. there already exist an account with the same id
                3. any of the parameters is invalid
        :raise DataAccessError: throws if db operation fails
        """
        if not (residence and gender and units):
            raise AppOperationError(f"Invalid parameters")
        if not self.account_id_exist(consumer_id):
            # log f"No account associated to id: [{consumer_id}]"
            raise AppOperationError(f"No account associated to the consumer")
        if self.is_consumer(consumer_id):
            #  log f"There already exits a consumer with id: [{consumer_id}]"
            raise AppOperationError(f"Account is already a consumer")
        # TODO:: verify height & weight
        self.db_proxy.add_consumer(consumer_id, residence, height, weight, units, gender, goal)



    def get_account_details(self, account_id: int):
        account: Account = self.db_proxy.get_account_by_id(account_id=account_id)
        if not account:
            raise AppOperationError(f"Invalid account id or email")
        return {'first_name':account.first_name,'last_name':account.last_name,'date_of_birth':date_to_str(account.date_of_birth)}


    # helper methods
    def is_email_registered(self, email):
        return self.db_proxy.has_account_with_email(email)

    def account_id_exist(self, account_id: int) -> bool:
        return self.db_proxy.has_account_with_id(account_id)

    def is_consumer(self, consumer_id: int) -> bool:
        return self.db_proxy.has_consumer(consumer_id)
