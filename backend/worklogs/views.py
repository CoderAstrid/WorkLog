from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
from .models import WorkLog
from .serializers import WorkLogSerializer

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_worklogs(request):
    logs = WorkLog.objects.all().values('id', 'user__username', 'date', 'content', 'notes')
    return JsonResponse(list(logs), safe=False)

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
