from voyager_system.domain.medicalCenter.Consumer import Consumer
from voyager_system.dal_DEPRECATED.db.DBSchemeSetup import *

class DBController:
    def __init__(self) -> None:
        self.engine = None
        self.session = None


    async def get_consumer(self,consumer_id):
        raise NotImplementedError("Should have implemented this")


    async def add_consumer(self, consumer: Consumer):
        consumer_dto = ConsumerDTO.from_consumer(consumer)
        self.session.add(consumer_dto)
        self.session.commit()
        raise NotImplementedError("Should have implemented this")
