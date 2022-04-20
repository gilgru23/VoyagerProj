from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

import server.service.GuestService as GuestService


# Create your views here.
def login_user(request: HttpRequest):
    keys = ['email', 'pwd']
    email, pwd = keys_to_values(request.POST, keys)
    user = authenticate(request, username=email, password=pwd)
    if user is not None:
        login(request, user)
        return HttpResponse("Successfully logged in")
    else:
        return HttpResponse("Failed to log in")

def logout_user(request: HttpRequest):
    logout(request)
    return HttpResponse("logged out")

@csrf_exempt
def register_user(request: HttpRequest):
    keys = ['email', 'pwd', 'phone', 'f_name', 'l_name', 'dob']
    email, pwd, phone, f_name, l_name, dob = keys_to_values(request.POST, keys)
    res = GuestService.create_account(email, pwd, phone, f_name, l_name, dob)
    return HttpResponse(res)


def create_consumer_profile(request: HttpRequest):
    id = get_acount_id(request)
    keys = ['residence', 'height', 'weight', 'units', 'gender', 'goal']
    residence, height, weight, units, gender, goal = keys_to_values(request.POST, keys)
    res = GuestService.create_consumer_profile(id, residence, height, weight, units, gender, goal)

#region helper
def get_acount_id(request: HttpRequest) -> int:
    #todo: implement!
    return 0

def keys_to_values(d:dict, keys):
    return [d[key] for key in keys]

#endregion