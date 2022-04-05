import asyncio


class IMapper:
    # class attribute
    engine = None
    session = None

    # instance init
    def __init__(self):
        # Init engine and session
        pass

    # methods
    async def get_consumer(self,consumer_id):
        raise NotImplementedError("Should have implemented this")


    async def add_consumer(self,consumer_id):
        raise NotImplementedError("Should have implemented this")


    async def update_consumer(self,consumer):
        raise NotImplementedError("Should have implemented this")


    async def delete_consumer(self,consumer):
        raise NotImplementedError("Should have implemented this")
