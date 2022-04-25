
# import voyager_system.data_access.database

from voyager_system.data_access.IStorage import IStorage


class DatabaseProxy(IStorage):
    def __init__(self, db_impl):
        super().__init__()
        self.db = db_impl

    def consumer_register_dispenser(self, consumer_id, dispenser_serial_number):
        return self.db.set_dispenser_consumer(dispenser_serial_number, consumer_id)


    async def get_consumer(self,consumer_id):
        raise NotImplementedError("Should have implemented this")