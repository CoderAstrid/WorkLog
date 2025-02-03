from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role', 'user')  # Default role = 'user'
        user = CustomUser.objects.create_user(**validated_data)
        user.role = role  # Assign the role properly
        user.save()
        return user
