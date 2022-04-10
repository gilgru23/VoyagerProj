from domain.medicalCenter.Consumer import Consumer


class ICacher:
    def __init__(self) -> None:
        pass


    def get_consumer_by_id(self, consumer_id):
        raise NotImplementedError("Should have implemented this")


    def add_consumer_to_cache(self, consumer: Consumer):
        raise NotImplementedError("Should have implemented this")
