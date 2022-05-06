from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

import voyager_system.service.ServiceSetup as service
import common.request_helper as rh


@csrf_exempt
def register_user(request: HttpRequest):
    keys = ['email', 'pwd', 'phone', 'f_name', 'l_name', 'dob']
    email, pwd, phone, f_name, l_name, dob = rh.keys_to_values(request, keys)
    res = service.get_guest_service().create_account(email, phone, f_name, l_name, dob)
    User.objects.create_user(email, email, pwd)
    return rh.result_to_response(res)

@csrf_exempt
def login_user(request: HttpRequest):
    keys = ['email', 'pwd']
    email, pwd = rh.keys_to_values(request, keys)
    user = authenticate(request, username=email, password=pwd)
    if user is not None:
        login(request, user)
        return HttpResponse("Successfully logged in")
    else:
        return HttpResponse("Failed to log in", status = rh.BAD_REQUEST_STATUS_CODE)

@csrf_exempt
def logout_user(request: HttpRequest):
    logout(request)
    return HttpResponse("logged out")

@csrf_exempt
def create_consumer_profile(request: HttpRequest):
    id = rh.get_acount_id(request)
    keys = ['residence', 'height', 'weight', 'units', 'gender', 'goal']
    residence, height, weight, units, gender, goal = rh.keys_to_values(request, keys)
    res = service.get_guest_service().create_consumer_profile(id, residence, height, weight, units, gender, goal)
    return rh.result_to_response(res)

