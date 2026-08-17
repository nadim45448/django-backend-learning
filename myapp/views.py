from django.shortcuts import render 
from django.http import HttpResponse

# Create your views here.

def index(request):
    # return HttpResponse('<h1> Welcome to django learning </h1>')

    # inspact request object
    # return HttpResponse(
    #     f"Method: {request.method}<br>"
    #     f"Path: {request.path}<br>"
    #     f"User Agent: {request.headers.get('User-Agent')}<br>"
    # )

    # query parameter
    name = request.GET.get('name')
    age = request.GET.get('age')
    return HttpResponse(
        f"Hello {name}, you are {age} years old."
    )


def hello(request):
    return HttpResponse("Hello from Django!")

# dynamic path parameter
def hello_user(request, name):
    return HttpResponse(
        f"Hello, {name}!"
    )
