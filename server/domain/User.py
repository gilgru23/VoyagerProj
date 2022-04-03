class User:
    # class attribute
    email = None
    phone = None
    first_name = None
    date_of_birth = None

    def __init__(self) -> None:
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
