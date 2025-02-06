from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import WorkLog
from .serializers import WorkLogSerializer
from django.http import HttpResponse
import pandas as pd
import openpyxl

@api_view(['POST'])
@permission_classes([IsAdminUser])
def export_worklogs(request):
    """Export selected work logs to an Excel file"""
    
    log_ids = request.data.get("selectedLogs", [])  # ✅ Expect only IDs

    if not isinstance(log_ids, list) or not all(isinstance(id, int) for id in log_ids):
        return HttpResponse("Invalid data format", status=400)  # ✅ Ensure it's a list of integers

    logs = WorkLog.objects.filter(id__in=log_ids).select_related("user")

    # Prepare data
    data = [
        {
            "Date": log.date.strftime("%Y-%m-%d"),
            "User ID": log.user.username,
            "Full Name": f"{log.user.first_name} {log.user.last_name}",
            "Work Content": log.content,
            "Notes": log.notes
        }
        for log in logs
    ]

    df = pd.DataFrame(data)

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="worklogs.xlsx"'

    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="WorkLogs")
        worksheet = writer.sheets["WorkLogs"]

        # ✅ Format for multiline text in Excel
        for i, col in enumerate(df.columns):
            col_width = max(df[col].astype(str).apply(len).max(), len(col)) + 5
            worksheet.column_dimensions[chr(65 + i)].width = col_width  # Adjust column width
            for row in range(2, len(df) + 2):
                worksheet.cell(row=row, column=i + 1).alignment = openpyxl.styles.Alignment(wrap_text=True)

    return response

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
    logs = WorkLog.objects.select_related("user").all().order_by('-date')
    serializer = WorkLogSerializer(logs, many=True)
    return Response(serializer.data)

### 🔹 2️⃣ Create a New Work Log
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_worklog(request):
    """Creates a new work log entry for the logged-in user."""
    print(request)
    data = request.data.copy()  # Make a mutable copy
    serializer = WorkLogSerializer(data=data)

    if serializer.is_valid():
        serializer.save(user=request.user)  # ✅ Assign user instance, not ID
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
@permission_classes([IsAdminUser])  # ✅ Only admins can delete logs
def delete_worklog(request, log_id):
    """Delete a specific work log (Admins only)"""
    print(f"Attempting to delete log ID: {log_id}")
    
    log = get_object_or_404(WorkLog, id=log_id)  # ✅ Remove user filter to allow admin deletion
    
    log.delete()
    return Response({"message": f"Work log {log_id} deleted successfully"}, status=204)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def worklogs(request):
    if request.user.is_staff:
        logs = WorkLog.objects.all().order_by('-date')
    else:
        logs = WorkLog.objects.filter(user=request.user).order_by('-date')

    if request.method == 'GET':
        serializer = WorkLogSerializer(logs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WorkLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
