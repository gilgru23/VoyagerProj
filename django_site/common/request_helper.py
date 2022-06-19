from django.http import HttpResponse, HttpRequest

from account_api.models import Account
import json

BAD_REQUEST_STATUS_CODE = 400


# todo: implement better, holding a dictionary of email to id, rather than referencing db
def get_acount_id(request: HttpRequest) -> int:
    email = request.user.username
    try:
        acct: Account = Account.objects.get(email=email)
        account_id = acct.pk
    except:
        account_id = -1
    return account_id


# get values of the POST request
def keys_to_values(request: HttpRequest, keys):
    # body_unicode = request.body.decode('utf-8')
    # body = request.POST
    body = json.loads(request.body)
    return [body[key] for key in keys]

# get parameters of the GET request
def get_parameters(request: HttpRequest, keys):
    params_dict = request.GET
    return [params_dict.get(key, '') for key in keys]


def result_to_response(res):
    (succeeded, val) = res
    if succeeded:
        if isinstance(val, str):
            return HttpResponse(val)
        elif isinstance(val, dict):
            return HttpResponse(json.dumps(val))
        elif isinstance(val, list):
            return HttpResponse(json.dumps(val))
        else:
            return HttpResponse(str(val))
    else:
        return HttpResponse(val, status=BAD_REQUEST_STATUS_CODE)


def error_str_to_response(err_str):
    try:
        err_str = err_str.strip("[\'\']")
    except Exception:
        pass
    return HttpResponse(err_str, status=BAD_REQUEST_STATUS_CODE)
