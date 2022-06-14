from django.http import HttpResponse, HttpRequest

from account_api.models import Account
import voyager_system.service.ManagerService as manager_service
import json

BAD_REQUEST_STATUS_CODE = 400



#todo: implement better, holding a dictionary of email to id, rather than referencing db
def get_acount_id(request: HttpRequest) -> int:
    email = request.user.username
    acct: Account = Account.objects.get(email=email)
    account_id = acct.pk
    # print('acct id is: ' + str(account_id))
    return account_id

def keys_to_values(request: HttpRequest, keys):
    # body_unicode = request.body.decode('utf-8')
    # body = request.POST
    body = json.loads(request.body)
    return [body[key] for key in keys]

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

