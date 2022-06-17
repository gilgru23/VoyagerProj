class AppOperationError(Exception):
    pass


class DataAccessError(Exception):
    pass


class ConcurrentUpdateError(Exception):
    pass
