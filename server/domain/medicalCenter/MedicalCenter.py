from dal.DummyMapper import DummyMapper
from dal.IMapper import IMapper


# @TODO: make this class a singleton (?)
class MedicalCenter:

    def __init__(self) -> None:
        self.object_mapper: IMapper = DummyMapper()
        pass

    async def get_consumer(self, consumer_id):
        await self.object_mapper.get_consumer(consumer_id)
        # @TODO: replace this with an actual method
