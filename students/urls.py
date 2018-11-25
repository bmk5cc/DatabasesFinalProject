"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('add_class/', views.add_class, name='add_class'),
    path('deleteClass/', views.deleteClass, name='deleteClass'),
    path('', views.index, name='index'),
    path('jobs/', views.jobs, name='jobs'),
    path('department/', views.department, name ='department')
]
