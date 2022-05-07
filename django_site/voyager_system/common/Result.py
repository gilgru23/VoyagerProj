

def failure(msg: str):
    return (False, msg)


def success(obj: object = None):
    return (True, obj)


def is_successful(res: tuple) -> bool:
    return res[0]


def is_failure(res: tuple) -> bool:
    return not res[0]


def get_value(res: tuple):
    if (not res) or (is_failure(res)):
        raise ValueError(f"wrong argument type received {res}")
    else:
        return res[1]
