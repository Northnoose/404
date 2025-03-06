
from rest_framework import serializers
from .models import User, UserPermission, Task, Module, UserTask, UserModule

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id', 'username', 'email', 'user_type']
        
class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta():
        model = UserPermission
        fields = '__all__'
        
        
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'description', 'task_object']


class ModuleSerializer(serializers.ModelSerializer):
    task = TaskSerializer()  

    class Meta:
        model = Module
        fields = ['id', 'task', 'description']

class UserTaskSerializer(serializers.ModelSerializer):
    user = UserSerializer()  
    task = TaskSerializer()
    class Meta:
        model = UserTask
        fields = ['user', 'task', 'score', 'finished']



class UserModuleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    module = ModuleSerializer() 
    class Meta:
        model = UserModule
        fields = ['user', 'module', 'score', 'finished']