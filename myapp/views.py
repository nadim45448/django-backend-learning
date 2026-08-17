from django.shortcuts import render 
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

products_data = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 900
    },
    {
        "id": 2,
        "name": "Keyboard",
        "price": 150
    },
    {
        "id": 3,
        "name": "Mouse",
        "price": 50
    }
]

def index(request):
    return HttpResponse('<h1> Welcome to django learning </h1>')

    # inspact request object
    # return HttpResponse(
    #     f"Method: {request.method}<br>"
    #     f"Path: {request.path}<br>"
    #     f"User Agent: {request.headers.get('User-Agent')}<br>"
    # )

    # query parameter
    # name = request.GET.get('name')
    # age = request.GET.get('age')
    # return HttpResponse(
    #     f"Hello {name}, you are {age} years old."
    # )


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
    
# GET vs POST
@csrf_exempt
def products(request):
    # read
    if request.method == "GET":
        return JsonResponse(products_data, safe=False)
    
    # create
    if request.method == "POST":
        data = json.loads(request.body)

        # input validation
        name = data.get('name')
        price = data.get('price')

        # 1. Check required fields
        if not name or price is None:
            return JsonResponse(
                {
                    "error":"name and price are required"
                },
                status=400
            )
        # 2. check name type
        if not isinstance(name, str):
            return JsonResponse(
                {"error":"name must be a string"},
                status=400
            )
        # 3. check price type
        if not isinstance(price, (int, float)):
            return JsonResponse(
                {"error":"price must be a n umber"},
                status=400
            )

        # 4. check price value
        if price<=0:
            return JsonResponse(
                {"error":"price must be greater than 0"},
                status=400
            )

        # generate a new id
        new_id = len(products_data) + 1

        # create the new product
        new_product = {
            "id":new_id,
            "name":name,
            "price":price
        }

        # add products to the products_data list
        products_data.append(new_product)

        # return the created product
        return JsonResponse(new_product, status=201)
    
        # everything is valid
        # return JsonResponse({
        #     # "message":"You sent a POST request"
        #     "message":"Products received",
        #     "name":data["name"],
        #     "price":data["price"]
        # })
    
    # Handle unsupported HTTP methods
    return JsonResponse(
        {"error":"Method not allowed"},
        status=405
        )
