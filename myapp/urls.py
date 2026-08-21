from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('hello/<str:name>/', views.hello_user, name='hello_user'),
    path('products/', views.products, name="products"),
    path('products/<int:product_id>/', views.product_details, name='product_details'),
    path('text/',views.text_input, name ="text_input"),
    path('counter/',views.counter, name="counter"),
    path('items/',views.items, name="items"),
    path('items/<int:item_id>/',views.item_details, name="item_details"),
    path('orders/',views.orders, name="orders"),
    path('item/create/',views.item_create, name="item_create"),
    path('item/list/',views.item_list, name="item_list"),
    path('item/',views.item, name="item"),
    path('item/<int:item_id>/',views.items_details, name="items_details"),
]