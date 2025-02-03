from rest_framework import serializers
from .models import WorkLog


class WorkLogSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)  # ✅ Include username

    class Meta:
        model = WorkLog
        fields = ['id', 'date', 'content', 'notes', 'username', 'first_name', 'last_name']  # ✅ Add "username"
