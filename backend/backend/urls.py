# from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),  # Add Django REST framework login/logout views
    path('api/', include('users.urls')),
    path('api/', include('worklogs.urls')),
]