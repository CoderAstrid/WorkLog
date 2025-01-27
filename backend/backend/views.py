from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from worklogs.models import WorkLog
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_worklogs(request):
    logs = WorkLog.objects.all().values('id', 'user__username', 'date', 'content', 'notes')
    return JsonResponse(list(logs), safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_users(request):
    users = User.objects.all().values('id', 'username', 'email', 'is_active', 'is_staff')
    return JsonResponse(list(users), safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_profile(request):
    admin_data = {
        "username": request.user.username,
        "email": request.user.email
    }
    return JsonResponse(admin_data)
