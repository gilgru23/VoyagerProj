

class DatabaseProxy:
    def __init__(self, db_impl, object_cache = None):
        super().__init__()
        self.db = db_impl
        self.object_cache = object_cache



    def get_account_by_id(self, user_id):
        raise NotImplementedError("Should have implemented this")

    def add_account(self, email, phone, first_name, last_name, date_of_birth):
        raise NotImplementedError("Should have implemented this")

    def get_account(self, email):
        raise NotImplementedError("Should have implemented this")


    def has_account_with_email(self, email):
        raise NotImplementedError("Should have implemented this")

    async def get_consumer(self,consumer_id):
        return self.db.get_consumer(consumer_id)

    def add_consumer(self, consumer_id, residence, height, weight, units, gender, goal):
        raise NotImplementedError("Should have implemented this")

    def update_consumer(self, consumer):
        pass

    def consumer_register_dispenser(self, consumer_id, dispenser_serial_number):
        return self.db.set_dispenser_consumer(dispenser_serial_number, consumer_id)

