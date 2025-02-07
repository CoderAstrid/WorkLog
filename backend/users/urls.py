from django.urls import path
from .views import login_user, register_user, forgot_password, reset_password, admin_users, admin_profile, user_profile, get_security_questions

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('reset-password/<str:token>/', reset_password, name='reset-password'),
    path('user/profile/', user_profile, name='user-profile'),
    path('user/security-questions/', get_security_questions, name='security-questions'),

    # Admin endpoints (Restricted to IsAdminUser)
    path('admin/users/', admin_users, name='admin-users'),
    path('admin/profile/', admin_profile, name='admin-profile'),
]
