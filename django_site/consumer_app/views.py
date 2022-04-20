from django.shortcuts import render
#everything below added by tzuri
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello Voyager Consumer!")