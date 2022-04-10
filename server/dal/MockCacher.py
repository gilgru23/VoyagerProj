
import domain.common.Result as Res
from dal.ICacher import ICacher
from domain.medicalCenter.Consumer import Consumer


class MockCacher(ICacher):
    def __init__(self) -> None:
        self.consumers_cache = dict()

    def get_consumer_by_id(self, consumer_id):
        if consumer_id not in self.consumers_cache:
            return Res.success(None)
        else:
            return Res.success(self.consumers_cache[consumer_id])

    def add_consumer_to_cache(self, consumer: Consumer):
        if consumer.id in self.consumers_cache:
            return Res.failure(f"Error add_consumer_to_cache: consumer [{consumer.id}] is already in cache!")
        else:
            self.consumers_cache[consumer.id] = consumer
            return Res.success()






