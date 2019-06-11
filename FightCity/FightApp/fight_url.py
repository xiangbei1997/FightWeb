from django.urls import path
from FightApp import views


urlpatterns = [
    path('home.html', views.home),
    path('order.html', views.order),
    path('register.html', views.register),
]