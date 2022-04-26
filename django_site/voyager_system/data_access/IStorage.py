from voyager_system.data_access.dtos import DispenserDto, ConsumerDto, AccountDto


class IStorage:

    # instance init
    def __init__(self):
        pass

    def set_dispenser_consumer(self,dispenser_serial_number, consumer_id):
        raise NotImplementedError("Should have implemented this")

    def get_consumer(self, account_id: int):
        raise NotImplementedError("Should have implemented this")

    # *********************

    # region Account
    def has_account_with_email(self, email):
        raise NotImplementedError("Should have implemented this")

    def add_account(self, email, f_name, l_name, phone, dob):
        raise NotImplementedError("Should have implemented this")

    def add_account(self, acct_dto: AccountDto):
        raise NotImplementedError("Should have implemented this")

    def get_account_by_email(self, email: str):
        raise NotImplementedError("Should have implemented this")

    def get_account_by_id(self, id: int):
        raise NotImplementedError("Should have implemented this")

    def update_account(self, account_dto: AccountDto):
        raise NotImplementedError("Should have implemented this")

    # endregion Account

    # region Consumer
    def add_consumer(self, id: int, residence: str, height: int, weight: int, units: str, gender: str, goal: any):
        raise NotImplementedError("Should have implemented this")

    def get_consumer(self, account_id: int):
        raise NotImplementedError("Should have implemented this")

    def update_consumer(self, consumer_dto: ConsumerDto):
        raise NotImplementedError("Should have implemented this")

    # dispenser
    def add_dispenser(self, serial_num: str, version: str):
        raise NotImplementedError("Should have implemented this")

    def get_dispenser(self, serial_num: str):
        raise NotImplementedError("Should have implemented this")

    # todo: depreciate, use update_dispenser instead
    def set_dispenser_consumer(self, serial_num: str, consumer_id: int):
        raise NotImplementedError("Should have implemented this")

    def update_dispenser(self, dispenser_dto: DispenserDto):
        raise NotImplementedError("Should have implemented this")
    # endregion Consumer

