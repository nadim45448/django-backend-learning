from itertools import product
from django.shortcuts import render 
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, Customer, Order
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ModelViewSet

from .serializers import ProductSerializer

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
    words = request.POST.get('text', '')
    word_count = len(words.split())
    return render(request, 'counter.html', {'word_count': word_count})

# connect API to the DB
@csrf_exempt
def items(request):
    if request.method == "GET":
        items = Product.objects.all()
        return JsonResponse(
            {
                "items":list(items.values("id","name","price"))
            }
        )
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON data"
            }, status=400)

        if "name" not in data or "price" not in data:
            return JsonResponse({
                "error": "name and price are required"
            }, status=400)
        
        if not data["name"]:
            return JsonResponse({
                "error": "name cannot be empty"
            }, status=400)
        
        if not isinstance(data["price"], (int, float)):
            return JsonResponse({
                "error": "price must be a number"
            }, status=400)
        
        if data["price"] <= 0:
            return JsonResponse({
                "error": "price must be greater than 0"
            }, status=400)

        item = Product.objects.create(
            name=data['name'],
            price=data['price']
        )
        return JsonResponse(
            {
                "item": {
                    "id": item.id,
                    "name": item.name,
                    "price": item.price
                }
            },
            status=201
        )
    
@csrf_exempt
def item_details(request, item_id):
    # item = Product.objects.get(id=item_id)
    item = get_object_or_404(Product, id=item_id)

    if request.method == "GET":
        return JsonResponse(
            {
                "item": {
                    "id": item.id,
                    "name": item.name,
                    "price": item.price
                }
            }
        )

    if request.method == "PATCH":

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON"
            }, status=400)

        if not data:
            return JsonResponse({
                "error": "At least one field is required"
            }, status=400)

        if "name" in data:
            if not isinstance(data["name"], str):
                return JsonResponse({
                    "error": "Name must be a string"
                }, status=400)
            item.name = data["name"]

        if "price" in data:
            if not isinstance(data["price"], (int, float)):
                return JsonResponse({
                    "error": "Price must be a number"
                }, status=400)
            item.price = data["price"]

        item.save()

        return JsonResponse({
            "id": item.id,
            "name": item.name,
            "price": item.price
        })

    if request.method == "DELETE":
        item.delete()
        return JsonResponse({
            "message": "Item deleted successfully"
        })

    # model relationships in an API
@csrf_exempt
def orders(request):

    if request.method == "POST":

        data = json.loads(request.body)

        customer = get_object_or_404(Customer, id=data["customer_id"])

        product = get_object_or_404(Product, id=data["product_id"])
        

        order = Order.objects.create(
            customer=customer,
            product=product
        )

        return JsonResponse({
            "id": order.id,
            "customer": order.customer.name,
            "product": order.product.name
        }, status=201)
    
@api_view(['POST'])
def item_create(request):

    serializer = ProductSerializer(
        data = request.data
    )

    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )
@api_view(['GET'])
def item_list(request):
    items = Product.objects.all()
    serializer = ProductSerializer(items, many=True)
    return Response(serializer.data)

# combine the above two views into a single view using @api_view(['GET', 'POST'])
@api_view(['GET', 'POST'])
def item(request):
    if request.method == "GET":
        items = Product.objects.all()
        serializer = ProductSerializer(items, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PATCH', 'DELETE'])
def items_details(request, item_id):
    item = get_object_or_404(Product, id=item_id)

    if request.method == "GET":
        serializer = ProductSerializer(item)
        return Response(serializer.data)
    
    elif request.method == "PATCH":
        serializer = ProductSerializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# DRF class-based views
# class ItemListView(APIView):
#     def get(self, request):
#         items = Product.objects.all()
#         serializer = ProductSerializer(items, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# DRF generic class-based views
class ItemListView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        print("Creating a new product")
        serializer.save()

# DRF class-based views
# class ItemDetailView(APIView):
#     def get_object(self, item_id):
#         return get_object_or_404(Product, id=item_id)

#     def get(self, request, item_id):
#         item = self.get_object(item_id)
#         serializer = ProductSerializer(item)
#         return Response(serializer.data)

#     def patch(self, request, item_id):
#         item = self.get_object(item_id)
#         serializer = ProductSerializer(item, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, item_id):
#         item = self.get_object(item_id)
#         item.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# DRF generic class-based views
class ItemDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'item_id'

# viewsets
# class ItemViewSet(ViewSet):
#     def list(self, request):
#         items = Product.objects.all()
#         serializer = ProductSerializer(items, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def retrieve(self, request, pk=None):
#         item = get_object_or_404(Product, id=pk)
#         serializer = ProductSerializer(item)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         item = get_object_or_404(Product, id=pk)
#         serializer = ProductSerializer(item, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def partial_update(self, request, pk=None):
#         item = get_object_or_404(Product, id=pk)
#         serializer = ProductSerializer(item, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def destroy(self, request, pk=None):
#         item = get_object_or_404(Product, id=pk)
#         item.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# DRF model viewsets
class ItemViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        print("Creating a new product")
        serializer.save()

    def perform_update(self, serializer):
        print("Updating a product")
        serializer.save()

    def perform_destroy(self, instance):
        print("Deleting a product")
        instance.delete()
        