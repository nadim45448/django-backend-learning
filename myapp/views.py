from django.shortcuts import render 
from django.http import HttpResponse, JsonResponse

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

# returning json from django
def product_details(request, product_id):
    return JsonResponse({
        "id":product_id,
        "name":"Laptop",
        "price":800
    })

def product_list(request):
    products_list = [
        {
            "id":1,
            "name":"Laptop",
            "price":900
        },
        {
            "id":2,
            "name":"Keyboard",
            "price":150
        },
        {
            "id": 3,
            "name": "Mouse",
            "price": 50
        }
    ]
    return JsonResponse(products_list, safe=False)
    
