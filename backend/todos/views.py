from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import date
from .models import Category, Task, Subtask
from .serializers import CategorySerializer, TaskSerializer, SubtaskSerializer

# ============ FUNCTION-BASED VIEWS ============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    """
    Returns task counts and status breakdown for the dashboard.
    """
    user = request.user
    tasks = Task.objects.filter(user=user, is_archived=False)
    
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    pending_tasks = tasks.filter(status='pending').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    
    today = date.today()
    overdue_tasks = tasks.filter(due_date__lt=today, status__in=['pending', 'in_progress']).count()
    
    return Response({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'overdue_tasks': overdue_tasks,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def today_tasks(request):
    """
    Returns tasks due today and overdue tasks.
    """
    user = request.user
    today = date.today()
    
    tasks_due_today = Task.objects.filter(
        user=user,
        due_date=today,
        is_archived=False
    )
    
    overdue_tasks = Task.objects.filter(
        user=user,
        due_date__lt=today,
        status__in=['pending', 'in_progress'],
        is_archived=False
    )
    
    return Response({
        'today': TaskSerializer(tasks_due_today, many=True).data,
        'overdue': TaskSerializer(overdue_tasks, many=True).data,
    }, status=status.HTTP_200_OK)

# ============ CLASS-BASED VIEWS (APIView) ============

class CategoryCollectionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        categories = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        return get_object_or_404(Category, pk=pk, user=user)
    
    def get(self, request, pk):
        category = self.get_object(pk, request.user)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        category = self.get_object(pk, request.user)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        category = self.get_object(pk, request.user)
        category.delete()
        return Response({"detail": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class TaskCollectionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        
        # Filtering
        category_id = request.query_params.get('category')
        status_filter = request.query_params.get('status')
        priority_filter = request.query_params.get('priority')
        is_archived = request.query_params.get('is_archived')
        
        if category_id:
            tasks = tasks.filter(category_id=category_id)
        if status_filter:
            tasks = tasks.filter(status=status_filter)
        if priority_filter:
            tasks = tasks.filter(priority=priority_filter)
        if is_archived is not None:
            tasks = tasks.filter(is_archived=is_archived.lower() == 'true')
        
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        return get_object_or_404(Task, pk=pk, user=user)
    
    def get(self, request, pk):
        task = self.get_object(pk, request.user)
        serializer = TaskSerializer(task, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        task = self.get_object(pk, request.user)
        serializer = TaskSerializer(task, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        task = self.get_object(pk, request.user)
        serializer = TaskSerializer(task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        task = self.get_object(pk, request.user)
        task.delete()
        return Response({"detail": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class SubtaskCollectionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        subtasks = Subtask.objects.filter(task=task, user=request.user)
        serializer = SubtaskSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        serializer = SubtaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubtaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        return get_object_or_404(Subtask, pk=pk, user=user)
    
    def patch(self, request, pk):
        subtask = self.get_object(pk, request.user)
        serializer = SubtaskSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        subtask = self.get_object(pk, request.user)
        subtask.delete()
        return Response({"detail": "Subtask deleted successfully."}, status=status.HTTP_204_NO_CONTENT)