# from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include

# Redirect root URL `/` to `/api/`
def redirect_root(request):
    return HttpResponseRedirect('/api/')

urlpatterns = [
    path('', redirect_root),  # Redirect root URL
    path('api-auth/', include('rest_framework.urls')),  # Add Django REST framework login/logout views
    path('api/', include('users.urls')),
    path('api/', include('worklogs.urls')),
]