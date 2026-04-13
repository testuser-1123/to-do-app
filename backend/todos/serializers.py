from rest_framework import serializers
from .models import Category, Task, Subtask

class CategorySerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'color', 'task_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_task_count(self, obj):
        return obj.tasks.count()

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'task', 'user', 'title', 'is_done', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    subtasks = SubtaskSerializer(many=True, read_only=True)
    subtask_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'user', 'category', 'category_name', 'category_color',
            'title', 'description', 'status', 'priority', 'due_date',
            'completed_at', 'is_archived', 'subtasks', 'subtask_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'completed_at', 'created_at', 'updated_at']
    
    def get_subtask_count(self, obj):
        return obj.subtasks.count()
    
    def validate_category(self, value):
        if value and value.user != self.context['request'].user:
            raise serializers.ValidationError("You can only assign your own categories.")
        return value
    
    def update(self, instance, validated_data):
        from django.utils import timezone
        
        # Handle completed_at timestamp
        new_status = validated_data.get('status', instance.status)
        if new_status == 'completed' and instance.status != 'completed':
            validated_data['completed_at'] = timezone.now()
        elif new_status != 'completed' and instance.status == 'completed':
            validated_data['completed_at'] = None
        
        return super().update(instance, validated_data)