class User:

    def __init__(self) -> None:
        # class attribute
        self.id = -1
        self.email = None
        self.phone = None
        self.first_name = None
        self.date_of_birth = None

        pass

    async def do_something(self, thing):
        raise NotImplementedError("replace this with an actual method")
        thing.do()

    async def login(self, thing):
        raise NotImplementedError("replace this with an actual method")
        thing.do()

    async def logout(self, thing):
        raise NotImplementedError("replace this with an actual method")
        thing.do()

    async def register(self, thing):
        raise NotImplementedError("replace this with an actual method")
        thing.do()
