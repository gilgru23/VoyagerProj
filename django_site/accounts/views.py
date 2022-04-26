from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json


USERNAME = "stupiduser"
PWD = "stupidpassword"

USERNAME_ADMIN = "admin"
PWD_ADMIN = "whoasked"

# Create your views here.


def login_user(request: HttpRequest):
    user = authenticate(request, username=USERNAME_ADMIN, password=PWD_ADMIN)
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
    # async def create_account(self, email: str, f_name: str, l_name: str, phone: str, pwd: str) -> str:
    body = json.loads(request.body)
    email = body['email']
    pwd = body['pwd']
    if User.objects.filter(username=email).exists():
        return HttpResponse("Email already registerred")

    user = User.objects.create_user(email, email, pwd)
    return HttpResponse("registerred!")


def domain_create_user(email):
    return False
