"""rightdirection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [

    path("", views.athenshome, name="index"),
    path("home", views.home, name="home"),
    path("add", views.add, name="add"),
    path("SalahTimes", views.SalahTimes, name="SalahTimes"),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'), 
    path('ajax/load-states/', views.load_states, name='ajax_load_states'), 
]
