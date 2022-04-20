from django.shortcuts import render
#everything below added by tzuri
from django.http import HttpResponse, HttpRequest

import common.request_helper as rh
import server.service.ConsumerService as consumer_service

def index(request):
    return HttpResponse("Hello Voyager Consumer!")

def register_dispenser(request: HttpRequest):
    account_id = rh.get_acount_id(request)
    serial_num = request.POST['serial_num']
    # todo: call consumer_service.