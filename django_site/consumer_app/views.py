from django.shortcuts import render
#everything below added by tzuri
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

import common.request_helper as rh
import server.service.ConsumerService as consumer_service

def index(request):
    return HttpResponse("Hello Voyager Consumer!")

@csrf_exempt
def register_dispenser(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    serial_num = request.POST['serial_num']
    res = consumer_service.register_dispenser(account_id, serial_num)
    return HttpResponse(res)