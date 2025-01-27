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
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class AdminWorkLogView(View):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        logs = WorkLog.objects.all().values('id', 'user__username', 'date', 'content', 'notes')
        return JsonResponse(list(logs), safe=False)

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        WorkLog.objects.create(
            user_id=data['user_id'],
            date=data['date'],
            content=data['content'],
            notes=data.get('notes', '')
        )
        return JsonResponse({"message": "Work log created successfully"}, status=201)

@method_decorator(login_required, name='dispatch')
class AdminUserManagementView(View):
    def get(self, request):
        if not request.user.is_staff:
            return JsonResponse({"error": "Unauthorized access"}, status=403)
        users = User.objects.all().values('id', 'username', 'email', 'is_active', 'is_staff')
        return JsonResponse(list(users), safe=False)

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return JsonResponse({"message": "User created successfully"}, status=201)

@method_decorator(login_required, name='dispatch')
class AdminProfileView(View):
    def get(self, request):
        admin_data = {
            "username": request.user.username,
            "email": request.user.email
        }
        return JsonResponse(admin_data)

    @csrf_exempt
    def put(self, request):
        data = json.loads(request.body)
        request.user.email = data['email']
        request.user.save()
        return JsonResponse({"message": "Profile updated successfully"})
