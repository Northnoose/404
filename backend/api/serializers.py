
from rest_framework import serializers
from .models import User, UserPermission

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id', 'username', 'email', 'user_type']
        
class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta():
        model = UserPermission
        fields = '__all__'
        