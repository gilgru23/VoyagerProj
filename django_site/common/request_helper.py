from django.http import HttpResponse, HttpRequest


def get_acount_id(request: HttpRequest) -> int:
    #todo: implement!
    return 0

def keys_to_values(request: HttpRequest, keys):
    body = request.POST
    return [body[key] for key in keys]

# def keys_to_values(d:dict, keys):
#     return [d[key] for key in keys]