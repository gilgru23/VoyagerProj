from django.http import HttpResponse, HttpRequest

from accounts.models import Account
import voyager_system.service.ManagerService as manager_service
import json

BAD_REQUEST_STATUS_CODE = 400



#todo: implement better, holding a dictionary of email to id, rather than referencing db
def get_acount_id(request: HttpRequest) -> int:
    email = request.user.username
    acct: Account = Account.objects.get(email=email)
    account_id = acct.pk
    print('acct id is: ' + str(account_id))
    return account_id

def keys_to_values(request: HttpRequest, keys):
    # body_unicode = request.body.decode('utf-8')
    body = json.loads(request.body)
    # body = request.POST
    return [body[key] for key in keys]

def result_to_response(res):
    (succeeded, val) = res
    if succeeded:
        return HttpResponse(val)
    else:
        print("got a bad request")
        print(val)
        return HttpResponse(val, status=BAD_REQUEST_STATUS_CODE)

