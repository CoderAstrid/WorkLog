from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import WorkLog
from .serializers import WorkLogSerializer, UserSerializer
import json

# User Authentication Views
@api_view(['POST'])
@permission_classes([])  # Remove authentication requirement for login
def login_user(request):
    print(request.data)
    user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username, 'role': 'admin' if user.is_staff else 'user'})
    return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def forgot_password(request):
    user = User.objects.filter(email=request.data.get('email')).first()
    if user:
        # In a real-world app, send an email with reset instructions
        return Response({"message": "Password reset link sent to email"})
    return Response({"error": "Email not found"}, status=400)

# Work Log Management Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_work_log(request):
    data = request.data.copy()
    data['user'] = request.user.id
    serializer = WorkLogSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_work_log(request, log_id):
    try:
        log = WorkLog.objects.get(id=log_id, user=request.user)
        log.delete()
        return Response({"message": "Work log deleted successfully"}, status=204)
    except WorkLog.DoesNotExist:
        return Response({"error": "Log not found"}, status=404)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def worklogs(request):
    if request.user.is_staff:
        logs = WorkLog.objects.all()
    else:
        logs = WorkLog.objects.filter(user=request.user)

    if request.method == 'GET':
        serializer = WorkLogSerializer(logs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WorkLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
