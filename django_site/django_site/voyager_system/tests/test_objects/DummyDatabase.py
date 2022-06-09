from voyager_system.data_access.IStorage import IStorage


class DummyDatabase(IStorage):


    def __init__(self, consumer_factory):
        super(DummyDatabase, self).__init__()
        self.consumer_factory = consumer_factory

    @staticmethod
    def consumer_error(consumer_id):
        return False, f"Error : consumer [{consumer_id}] not found!"

    # methods
    async def get_consumer(self,consumer_id):
        print("DummyMapper: get_consumer was called")
        print(f"Here is consumer #{consumer_id}!")

        # failure example
        # if False:
        #     self.consumer_error(consumer_id)

        return self.consumer_factory(consumer_id)


    def set_dispenser_consumer(self, dispenser_serial_number, consumer_id):
        raise NotImplementedError("Should have implemented this")