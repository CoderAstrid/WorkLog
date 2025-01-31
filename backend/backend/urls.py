# from django.contrib import admin
from django.urls import path, include
# from worklogs.views import (
#     login_user, register_user, forgot_password,
#     add_work_log, delete_work_log, worklogs, reset_password
# )
# from backend.views import admin_worklogs, admin_users, admin_profile

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),  # Add Django REST framework login/logout views
    path('api/', include('users.urls')),
    path('api/', include('worklogs.urls')),
]