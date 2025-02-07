from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
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
import random
from django.utils.timezone import now, timedelta

# Store reset tokens
password_reset_tokens = {}

SECURITY_QUESTIONS = [
    "What is the name of your first pet?",
    "In what city were you born?",
    "What was the name of your elementary school?",
    "What was the first concert you attended?",
    "What is the title of your favorite book?",
    "What was the first movie you watched in a theater?",
    "What is the name of your childhood best friend?",
    "What was your first job?",
    "What is the name of your favorite teacher?",
    "What was the make and model of your first car?"
]

@api_view(['GET'])
def get_security_questions(request):
    """Returns predefined security questions"""
    return Response({"questions": SECURITY_QUESTIONS})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_password_reset_request(request):
    user = CustomUser.objects.get(username=request.data.get("username"))

    # Check if the reset is locked due to failed attempts
    if user.lock_until and now() < user.lock_until:
        return Response({"error": "Too many failed attempts. Try again later."}, status=403)

    # Select 2 random questions
    questions = random.sample(
        [
            (user.security_question_1, user.security_answer_1),
            (user.security_question_2, user.security_answer_2),
            (user.security_question_3, user.security_answer_3),
        ],
        2
    )
    
    return Response({
        "question_1": questions[0][0],
        "question_2": questions[1][0],
    })

@api_view(['POST'])
@permission_classes([IsAdminUser])
def verify_security_answers(request):
    user = CustomUser.objects.get(username=request.data.get("username"))
    answer_1 = request.data.get("answer_1")
    answer_2 = request.data.get("answer_2")

    # Check answers
    correct_answers = [
        user.security_answer_1.lower(),
        user.security_answer_2.lower(),
        user.security_answer_3.lower()
    ]

    if answer_1.lower() in correct_answers and answer_2.lower() in correct_answers:
        # Reset failed attempts
        user.failed_attempts = 0
        user.lock_until = None
        user.save()
        return Response({"message": "Security answers correct. You can now reset your password."})

    # If incorrect, increase failed attempts
    user.failed_attempts += 1
    if user.failed_attempts >= 3:
        user.lock_until = now() + timedelta(minutes=30)  # Lock for 30 min
    user.save()

    return Response({"error": "Incorrect answers. Try again."}, status=403)

@api_view(['POST'])
def update_security_questions(request):
    user = request.user
    data = request.data

    user.security_question_1 = data.get("security_question_1")
    user.security_answer_1 = data.get("security_answer_1")
    user.security_question_2 = data.get("security_question_2")
    user.security_answer_2 = data.get("security_answer_2")
    user.security_question_3 = data.get("security_question_3")
    user.security_answer_3 = data.get("security_answer_3")

    user.save()
    return Response({"message": "Security questions updated successfully."})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_user_password_reset(request):
    user = CustomUser.objects.get(email=request.data.get("email"))
    
    # Send email to admin
    send_mail(
        "Password Reset Request",
        f"User {user.username} has requested a password reset. Approve at /admin/usermanagement",
        "admin@example.com",
        ["admin@example.com"],
    )

    return Response({"message": "Password reset request sent to admin."})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_password_reset(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    reset_url = f"http://yourfrontend.com/reset-password/{user_id}"
    
    return Response({"reset_url": reset_url})

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
    first_name = request.data.get("first_name", "").strip()
    last_name = request.data.get("last_name", "").strip()
    is_admin = request.data.get("is_admin", False)  # Ensure admin checkbox is processed

    print(f"Registering User: {username}, Email: {email}, is_admin: {is_admin}")

    # Check if username already exists
    if CustomUser.objects.filter(username=username).exists():
        return Response({"error": "This ID is already taken."}, status=400)

    # Ensure only one admin exists
    admin_exists = CustomUser.objects.filter(is_staff=True).exists()
    if is_admin and admin_exists:
        return Response({"error": "Only one admin account is allowed."}, status=400)

    try:
        # Create a new user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        print(user)
        # Set as admin only if:
        # 1️⃣ The checkbox was checked **AND** it's the first admin user
        if is_admin and not admin_exists:
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
    users = CustomUser.objects.all().values('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff')
    return JsonResponse(list(users), safe=False)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_profile(request):
    admin_data = {
        "id": request.user.id,
        "username": request.user.username,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "role": "admin" if request.user.is_staff else "user"
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
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": "admin" if user.is_staff else "user"
        })

    elif request.method == "PUT":
        data = request.data
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        if "password" in data and data["password"]:
            user.set_password(data["password"])

        user.save()
        return Response({"message": "Profile updated successfully"})