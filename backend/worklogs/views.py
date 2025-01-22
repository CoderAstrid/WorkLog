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

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def worklogs(request):
    try:
        logs = WorkLog.objects.filter(user=request.user)
        serializer = WorkLogSerializer(logs, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)