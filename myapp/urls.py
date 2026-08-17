from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('hello/<str:name>/', views.hello_user, name='hello_user'),
]