from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(response):
    return HttpResponse("<h1>tech with tim!</hi>")
def v1(response):
    return HttpResponse("<h1>You see view1!</hi>")