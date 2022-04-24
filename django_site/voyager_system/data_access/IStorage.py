
class IStorage:

    # instance init
    def __init__(self):
        pass

    def set_dispenser_consumer(self,dispenser_serial_number, consumer_id):
        raise NotImplementedError("Should have implemented this")

    def get_consumer(self, account_id: int):
        raise NotImplementedError("Should have implemented this")
