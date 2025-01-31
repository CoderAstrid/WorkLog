from django.urls import path
from .views import worklogs, add_work_log, delete_work_log, admin_worklogs

urlpatterns = [
    path('worklogs/', worklogs, name='worklogs'),
    path('worklogs/add/', add_work_log, name='add-work-log'),
    path('worklogs/delete/<int:log_id>/', delete_work_log, name='delete-work-log'),

    path('admin/worklogs/', admin_worklogs, name='admin-worklogs'),
]
