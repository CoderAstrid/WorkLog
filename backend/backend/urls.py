"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from worklogs.views import login_user, register_user, forgot_password, add_work_log, worklogs

router = DefaultRouter()

urlpatterns = [
    path('api/login/', login_user),
    path('api/register/', register_user),
    path('api/forgot-password/', forgot_password),
    path('api/add_work_log/', add_work_log),
    path('api/worklogs/', worklogs, name='worklogs'),
]
