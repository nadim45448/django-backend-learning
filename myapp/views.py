from django.shortcuts import render 
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse('<h1> Welcome to django learning </h1>')

def hello(request):
    return HttpResponse("Hello from Django!")
