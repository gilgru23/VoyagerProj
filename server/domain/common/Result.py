

def failure(msg: str):
    return (False, msg)


def success(res: object = None):
    return (True, res)