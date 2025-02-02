from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
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
    """Registers a new user, ensuring only one admin can be created automatically."""
    
    username = request.data.get("username", "").strip()
    email = request.data.get("email", "").strip()
    password = request.data.get("password", "").strip()

    # Check if username already exists
    if CustomUser.objects.filter(username=username).exists():
        return Response({"error": "This ID is already taken."}, status=400)

    # Ensure no duplicate admin accounts
    if CustomUser.objects.filter(is_staff=True).count() >= 1:
        return Response({"error": "Only one admin accounts are allowed."}, status=400)

    try:
        # Create a new user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Automatically set the first registered user as an admin
        if not CustomUser.objects.filter(is_staff=True).exists():
            user.is_staff = True
            user.is_superuser = True
            user.save()

        return Response({"message": "User registered successfully."}, status=201)
    except IntegrityError:
        return Response({"error": "User with this email already exists."}, status=400)
    except ValidationError as e:
        return Response({"error": str(e)}, status=400)
    

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
    users = CustomUser.objects.all().values('id', 'username', 'email', 'is_active', 'is_staff')
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