import re
from voyager_system.domain.common.Util import AppOperationError

from voyager_system.domain.medicalCenter.MedicalCenter import MedicalCenter
from voyager_system.domain.DatabaseProxy import DatabaseProxy



class SystemManagement:

    def __init__(self, medical_center: MedicalCenter, db_proxy: DatabaseProxy) -> None:
        self.med_center: MedicalCenter = medical_center
        self.db_proxy: DatabaseProxy = db_proxy



    EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    # todo: handle phone number
    def create_account(self, email, phone, f_name, l_name, dob) -> str:
        if not re.search(self.EMAIL_REGEX, email):
            raise AppOperationError(f"Invalid parameters")
        if not (email and phone and f_name and l_name and dob):
            raise AppOperationError(f"Invalid parameters")
        if self.is_email_registered(email):
            #  log f"There already exits an account with email: [{email}]"
            raise AppOperationError(f"There already exits an account with email: [{email}]")
        self.db_proxy.add_account(email, phone, f_name, l_name, dob)


    def create_consumer_profile(self, consumer_id: int, residence: str, height: int, weight: int,
                                units, gender, goal: any):
        """
        creates a new Consumer for an Account in the system

        :param consumer_id: id of the account
        :param residence: string describing consumer's place of residence
        :param height: int describing the height of the consumer
        :param weight: int describing the weight of the consumer
        :param units: (pre defined) string describing the units of the measurements
        :param gender: string describing consumer's gender
        :param goal: string describing consumer goals for using the system
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


    # helper methods
    def is_email_registered(self, email):
        return self.db_proxy.has_account_with_email(email)

    def account_id_exist(self, account_id: int) -> bool:
        return self.db_proxy.has_account_with_id(account_id)

    def is_consumer(self, consumer_id: int) -> bool:
        return self.db_proxy.has_consumer(consumer_id)
