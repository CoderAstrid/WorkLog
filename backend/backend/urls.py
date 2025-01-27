# from django.contrib import admin
from django.urls import path, include
from worklogs.views import (
    login_user, register_user, forgot_password,
    add_work_log, delete_work_log, worklogs
)
from backend.views import admin_worklogs, admin_users, admin_profile

urlpatterns = [
    path('api/login/', login_user, name='login'),
    path('api/register/', register_user, name='register'),
    path('api/forgot-password/', forgot_password, name='forgot-password'),
    path('api/worklogs/', worklogs, name='worklogs'),
    path('api/worklogs/add/', add_work_log, name='add-work-log'),
    path('api/worklogs/delete/<int:log_id>/', delete_work_log, name='delete-work-log'),

    path('api/admin/worklogs/', admin_worklogs, name='admin-worklogs'),
    path('api/admin/users/', admin_users, name='admin-users'),
    path('api/admin/profile/', admin_profile, name='admin-profile'),

    path('api-auth/', include('rest_framework.urls')),  # Add Django REST framework login/logout views
]