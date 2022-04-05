from dal.DummyMapper import DummyMapper
from dal.IMapper import IMapper
from domain.medicalCenter.Consumer import Consumer


# @TODO: make this class a singleton (?)
class MedicalCenter:

    def __init__(self) -> None:
        self.object_mapper: IMapper = DummyMapper()
        pass

    def get_consumer(self, consumer_id):
        self.object_mapper.get_consumer(consumer_id)
        # @TODO: replace this with an actual method
