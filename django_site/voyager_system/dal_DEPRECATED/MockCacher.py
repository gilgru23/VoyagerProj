
from voyager_system.dal_DEPRECATED.ICacher import ICacher
from voyager_system.common.ErrorTypes import DataAccessError
from voyager_system.domain.medical_center.Consumer import Consumer


class MockCacher(ICacher):
    def __init__(self) -> None:
        super().__init__()
        self.consumers_cache = dict()

    async def get_consumer_by_id(self, consumer_id):
        if consumer_id not in self.consumers_cache:
            return None
        else:
            return self.consumers_cache[consumer_id]

    async def add_consumer_to_cache(self, consumer: Consumer):
        if consumer.id in self.consumers_cache:
            raise DataAccessError(f"Error add_consumer_to_cache: consumer [{consumer.id}] is already in cache!")
        self.consumers_cache[consumer.id] = consumer





