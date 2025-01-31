from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import WorkLog
from .serializers import WorkLogSerializer

### 🔹 1️⃣ Fetch All Work Logs for the Logged-in User
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_worklogs(request):
    """Retrieve all work logs for the authenticated user"""
    logs = WorkLog.objects.filter(user=request.user).order_by('-date')
    serializer = WorkLogSerializer(logs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_worklogs(request):
    logs = WorkLog.objects.all().values('id', 'user__username', 'date', 'content', 'notes')
    return JsonResponse(list(logs), safe=False)

### 🔹 2️⃣ Create a New Work Log
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_worklog(request):
    """Add a new work log for the logged-in user"""
    data = request.data.copy()
    data['user'] = request.user.id  # Set the user automatically
    serializer = WorkLogSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

### 🔹 3️⃣ Update an Existing Work Log
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_worklog(request, log_id):
    """Update a specific work log"""
    log = get_object_or_404(WorkLog, id=log_id, user=request.user)
    serializer = WorkLogSerializer(log, data=request.data, partial=True)  # Partial update allowed

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_worklog(request, log_id):
    """Delete a specific work log"""
    log = get_object_or_404(WorkLog, id=log_id, user=request.user)
    log.delete()
    return Response({"message": "Work log deleted successfully"}, status=204)

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
