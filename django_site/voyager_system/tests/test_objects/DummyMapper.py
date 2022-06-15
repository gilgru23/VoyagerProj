
class DummyMapper:

    # instance init
    def __init__(self, consumer_factory):
        super(DummyMapper, self).__init__()
        self.consumer_factory = consumer_factory

    @staticmethod
    def consumer_error(consumer_id):
        return False, f"Error : consumer [{consumer_id}] not found!"

    # methods
    def get_consumer(self,consumer_id):
        print("DummyMapper: get_consumer was called")

        # failure example
        # if False:
        #     self.consumer_error(consumer_id)

        return self.consumer_factory(consumer_id)


    def add_consumer(self,consumer_id):
        print("DummyMapper: add_consumer was called!")


    def update_consumer(self,consumer):
        print("DummyMapper: update_consumer was called!")


    def delete_consumer(self,consumer):
        print("DummyMapper: delete_consumer was called!")

    #general user
    def add_account(self, email: str, f_name: str, l_name: str, phone: str, pwd: str):
        print("DummyMapper: add_account was called!")

    def get_account(self, email: str):
        print("DummyMapper: get_account was called!")

    def get_account_by_id(self, user_id: int):
        print("DummyMapper: get_account_by_id was called!")
