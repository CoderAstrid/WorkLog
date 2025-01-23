from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import WorkLog
from .serializers import WorkLogSerializer

@api_view(['POST'])
def login_user(request):
    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User registered successfully"})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def forgot_password(request):
    user = User.objects.filter(email=request.data['email']).first()
    if user:
        # In a real-world app, send an email with reset instructions
        return Response({"message": "Password reset link sent to email"})
    return Response({"error": "Email not found"}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_work_log(request):
    data = request.data.copy()
    data['user'] = request.user.id  # Automatically set the logged-in user
    serializer = WorkLogSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def worklogs(request):
    if request.user.is_staff:  # Admin user
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