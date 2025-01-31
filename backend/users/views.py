from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import uuid
from django.http import JsonResponse

# Store reset tokens
password_reset_tokens = {}

@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_list(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# User Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    print(request.data)
    user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username, 'role': 'admin' if user.is_staff else 'user'})
    return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Registers a new user, ensuring no duplicate admin accounts."""    
    existing_admin = CustomUser.objects.filter(is_staff=True).exists()
    username = request.data.get('username')
    if CustomUser.objects.filter(username=username).exists():
        return Response({"error": "This ID is already taken"}, status=400)
    if request.data.get('is_admin') and existing_admin:
        return Response({"error": "Admin already exists"}, status=400)

    if CustomUser.objects.filter(username=request.data['username']).exists():
        return Response({"error": "User with this ID already exists"}, status=400)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if request.data.get('is_admin'):
            user.is_staff = True
            user.save()
        return Response({"message": "User registered successfully"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def forgot_password(request):
    user = CustomUser.objects.filter(email=request.data.get('email')).first()
    if user:
        reset_token = str(uuid.uuid4())
        password_reset_tokens[reset_token] = user.username
        reset_url = f"http://localhost:8080/reset-password/{reset_token}"
        send_mail(
            "Password Reset",
            f"Click the link to reset your password: {reset_url}",
            "admin@company.com",
            [user.email],
        )
        return Response({"message": "Password reset link sent to email"})
    return Response({"error": "Email not found"}, status=400)

@api_view(['POST'])
def reset_password(request, token):
    username = password_reset_tokens.get(token)
    if not username:
        return Response({"error": "Invalid token"}, status=400)
    
    user = CustomUser.objects.get(username=username)
    user.set_password(request.data['new_password'])
    user.save()
    del password_reset_tokens[token]
    return Response({"message": "Password reset successfully"})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_users(request):
    users = CustomUser.objects.all().values('id', 'username', 'email', 'is_active', 'role')
    return JsonResponse(list(users), safe=False)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_profile(request):
    admin_data = {
        "username": request.user.username,
        "email": request.user.email
    }
    return JsonResponse(admin_data)

@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Handles retrieving and updating user profiles"""
    user = request.user

    if request.method == "GET":
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": "admin" if user.is_staff else "user"
        })

    elif request.method == "PUT":
        data = request.data
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)

        if "password" in data and data["password"]:
            user.set_password(data["password"])

        user.save()
        return Response({"message": "Profile updated successfully"})