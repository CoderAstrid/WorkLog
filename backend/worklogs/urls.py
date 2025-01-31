from django.urls import path
from .views import get_worklogs, add_worklog, update_worklog, delete_worklog, admin_worklogs

urlpatterns = [
    path('worklogs/', get_worklogs, name='get-worklogs'),
    path('worklogs/add/', add_worklog, name='add-worklog'),
    path('worklogs/<int:log_id>/update/', update_worklog, name='update-worklog'),
    path('worklogs/<int:log_id>/delete/', delete_worklog, name='delete-worklog'),

    path('admin/worklogs/', admin_worklogs, name='admin-worklogs'),
]
