from django.shortcuts import render
#everything below added by tzuri
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

import common.request_helper as rh
import voyager_system.service.ServiceSetup as service

def index(request):
    return HttpResponse("Hello Voyager Consumer!")

'''

create_consumer_profile, register_dispenser, register_pod, dose
get_recomendation (ret podtype)
set_dosing_reminder
set_schedule/get_schedule
get_pods_of_consumer
'''

@csrf_exempt
def register_dispenser(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    keys = ['serial_num']
    serial_num, = rh.keys_to_values(request, keys)
    res = service.get_consumer_service().register_dispenser_to_consumer(account_id, serial_num)
    return rh.result_to_response(res)

@csrf_exempt
def register_pod(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    keys = ['serial_num']
    serial_num, = rh.keys_to_values(request, keys)
    res = service.get_consumer_service().register_pod_to_consumer(account_id, serial_num, "HARD_CODED_POD_TYPE")
    return rh.result_to_response(res)

@csrf_exempt
def dose(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    keys = ['pod', 'amount', 'units']
    pod, amount, units = rh.keys_to_values(request, keys)
    res = service.get_consumer_service().dose(account_id, pod, amount, units)
    return rh.result_to_response(res)


@csrf_exempt
def get_recomendation(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    res = service.get_consumer_service().get_recomendation(account_id)
    return rh.result_to_response(res)   

@csrf_exempt
def set_dosing_reminder(request: HttpRequest):
    pass

@csrf_exempt
def set_regimen(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    res = service.get_consumer_service().set_regimen(account_id)
    return rh.result_to_response(res)   

@csrf_exempt
def get_regimen(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    res = service.get_consumer_service().get_regimen(account_id)
    return rh.result_to_response(res)   

@csrf_exempt
def get_pods_of_consumer(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    res = service.get_consumer_service().get_consumers_pods(account_id)
    return rh.result_to_response(res)   


