import re
from voyager_system.common.ErrorTypes import AppOperationError
from voyager_system.common.DateTimeFormats import date_to_str
from voyager_system.domain.medical_center.MedicalCenter import MedicalCenter
from voyager_system.data_access.DatabaseProxy import DatabaseProxy

import logging
from voyager_system.domain.system_management.Account import Account


class SystemManagement:

    def __init__(self, medical_center: MedicalCenter, db_proxy: DatabaseProxy) -> None:
        self.med_center: MedicalCenter = medical_center
        self.db_proxy: DatabaseProxy = db_proxy
        self.logger = logging.getLogger('voyager.domain')

    EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    # todo: handle phone number
    def create_account(self, email, phone, f_name, l_name, dob):
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
        if not (email and phone and f_name and l_name and dob):
            err_str = f'invalid registration parameters [email:{email}, phone:{phone}, first name:{f_name}, last name: {l_name}]'
            self.logger.debug(err_str)
            raise AppOperationError(err_str)
        if not re.search(self.EMAIL_REGEX, email):
            err_str = f'invalid registration email [{email}]'
            self.logger.debug(err_str)
            raise AppOperationError(err_str)
        if self.is_email_registered(email):
            err_str = f"There already exits an account with email: [{email}]"
            self.logger.info(err_str)
            raise AppOperationError(err_str)
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
                2. there already exist a consumer with the same id
                3. any of the parameters is invalid
        :raise DataAccessError: throws if db operation fails
        """
        if not (residence and gender and units):
            err_str = f'invalid registration parameters (residence/ gender / units)'
            self.logger.debug(err_str)
            raise AppOperationError(err_str)
        if not self.account_id_exist(consumer_id):
            err_str = f"No account associated to id: [{consumer_id}]"
            self.logger.info(err_str)
            raise AppOperationError(f"No account associated to the given id")
        if self.is_consumer(consumer_id):
            err_str = f"There already exits a consumer with account id: [{consumer_id}]"
            self.logger.info(err_str)
            raise AppOperationError(f"Account is already a consumer")
        self.db_proxy.add_consumer(consumer_id, residence, height, weight, units, gender, goal)


    def create_caregiver_profile(self, caregiver_id: int):
        """
        creates a new Caregiver profile for an Account in the system

        :param caregiver_id: int - id of the account
        :return: None
        :raise AppOperationError: throws if any of the following occur:
                1. an account with the same id doesnt exit
                2. there already exist an account with the same id
        :raise DataAccessError: throws if db operation fails
        """
        if not self.account_id_exist(caregiver_id):
            err_str = f"No account associated to id: [{caregiver_id}]"
            self.logger.info(err_str)
            raise AppOperationError(f"No account associated to the given id")
        if self.is_caregiver(caregiver_id):
            err_str = f"There already exits a caregiver with id: [{caregiver_id}]"
            self.logger.info(err_str)
            raise AppOperationError(f"Account is already a caregiver")
        self.db_proxy.add_caregiver(caregiver_id)

    def get_account_details(self, account_id: int):
        account: Account = self.db_proxy.get_account_by_id(account_id=account_id)
        if not account:
            raise AppOperationError(f"Invalid account id or email")
        return {'first_name': account.first_name, 'last_name': account.last_name,
                'date_of_birth': date_to_str(account.date_of_birth)}

    # helper methods
    def is_email_registered(self, email):
        return self.db_proxy.has_account_with_email(email)

    def account_id_exist(self, account_id: int) -> bool:
        return self.db_proxy.has_account_with_id(account_id)

    def is_consumer(self, consumer_id: int) -> bool:
        return self.db_proxy.has_consumer(consumer_id)

    def is_caregiver(self, caregiver_id: int) -> bool:
        return self.db_proxy.has_caregiver(caregiver_id)
