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
    # return HttpResponse('<h1> Welcome to django learning </h1>')

    # send dynamic data to the template
    context ={
        'name':"Nadim",
        'nationality':'Bangladeshi'

    }
    return render(request, 'index.html', context)

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
@csrf_exempt
def product_details(request, product_id):

    # dummy data
    # return JsonResponse({
    #     "id":product_id,
    #     "name":"Laptop",
    #     "price":800
    # })

    for product in products_data:
        if product["id"] == product_id:
            # read one
            if request.method == "GET":
                return JsonResponse(product)
            # update
            if request.method =="PATCH":
                data = json.loads(request.body)
                if "price" in data:
                    price = data["price"]

                    if not isinstance(price,(int,float)):
                        return JsonResponse(
                            {"error":"price must be a number"},
                            status=400
                        )
                    if price<=0:
                        return JsonResponse(
                            {
                                "error":"Price must be greater than 0"
                            },
                            status = 400
                        )
                    product["price"] = price

                if "name" in data:
                    name = data["name"]
                    if not isinstance(name, str):
                        return JsonResponse(
                            {"error":"Name must be a string"},
                            status=400
                        )
                    if not name:
                        return JsonResponse(
                            {"error":"name cannot be empty"},
                            status=400
                        )
                    product["name"] = name
                return JsonResponse(product)
            
            # delete product
            if request.method == "DELETE":
                products_data.remove(product)

                return JsonResponse({
                    "error":"Product deleted successfully"
                })
            

    return JsonResponse(
            {"error":"Product not found"},
             status=404
        )
    
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

def text_input(request):
    return render(request, 'text-input.html')

def counter(request):
    words = request.GET.get('text', '')
    word_count = len(words.split())
    return render(request, 'counter.html', {'word_count': word_count})
