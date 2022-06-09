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
    keys = ['serial_num', 'version']
    serial_num, version = rh.keys_to_values(request, keys)
    res = service.get_consumer_service().register_dispenser_to_consumer(account_id, serial_num, version)
    return rh.result_to_response(res)

@csrf_exempt
def register_pod(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    keys = ['serial_num','pod_type']
    serial_num, pod_type = rh.keys_to_values(request, keys)
    # res = service.get_consumer_service().register_pod_to_consumer(account_id, serial_num, "HARD_CODED_POD_TYPE")
    res = service.get_consumer_service().register_pod_to_consumer(account_id, serial_num, pod_type)
    return rh.result_to_response(res)

@csrf_exempt
def dose(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    keys = ['pod_serial_num', 'amount', 'time']
    pod_serial_num, amount, time = rh.keys_to_values(request, keys)
    res = service.get_consumer_service().consumer_dose(account_id, pod_serial_num, amount, time)
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
def get_dosing_history(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    res = service.get_consumer_service().get_consumer_dosing_history(account_id)
    return rh.result_to_response(res)

@csrf_exempt
def get_pods_of_consumer(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    res = service.get_consumer_service().get_consumer_pods(account_id)
    return rh.result_to_response(res)

@csrf_exempt
def get_dispensers_of_consumer(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    res = service.get_consumer_service().get_consumer_dispensers(account_id)
    return rh.result_to_response(res)

@csrf_exempt
def provide_feedback(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    keys = ['dosing_id', 'rating', 'comment']
    dosing_id, rating, comment = rh.keys_to_values(request, keys)
    res = service.get_consumer_service().provide_feedback_to_dosing(account_id, dosing_id, rating, comment)
    return rh.result_to_response(res)


@csrf_exempt
def get_feedback_for_dosing(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    keys = ['dosing_id']
    dosing_id, = rh.keys_to_values(request, keys)
    res = service.get_consumer_service().get_feedback_for_dosing(account_id, dosing_id)
    return rh.result_to_response(res)


