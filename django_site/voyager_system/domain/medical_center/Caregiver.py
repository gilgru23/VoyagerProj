from voyager_system.common.ErrorTypes import AppOperationError
from voyager_system.domain.medical_center.Consumer import Consumer
from voyager_system.domain.system_management.Account import Account

class Caregiver(Account):

    def __init__(self) -> None:
        super().__init__()
        self.consumers = []  # list of associated consumers' ids.  (n-to-m relationship)

    def add_consumer(self,consumer: Consumer):
        # filtered_consumers = [c for c in self.consumers if c.id == consumer.id]
        # if filtered_consumers:
        #     raise AppOperationError(
        #         f"Error: caregiver register consumer - unable to register consumer [id - {consumer.id}] to caregiver [id {self.id}]")
        # self.consumers.insert(0, consumer)
        consumer_id = consumer.id
        filtered_consumers = [cid for cid in self.consumers if cid == consumer_id]
        if filtered_consumers:
            raise AppOperationError(
                f"Error: caregiver register consumer - unable to register consumer [id - {consumer_id}] to caregiver [id {self.id}]")
        self.consumers.insert(0, consumer_id)

    def get_consumers(self):
        return self.consumers.copy()

    def has_consumer(self, consumer_id: int):
        filtered_consumers = [cid for cid in self.consumers if cid == consumer_id]
        return len(filtered_consumers) == 1

