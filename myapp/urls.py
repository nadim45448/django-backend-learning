from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('hello/<str:name>/', views.hello_user, name='hello_user'),
    path('products/',views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_details, name='product_details'),
   
]