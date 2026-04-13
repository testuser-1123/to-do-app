from django.urls import path
from .views import (
    dashboard_summary,
    today_tasks,
    CategoryCollectionAPIView,
    CategoryDetailAPIView,
    TaskCollectionAPIView,
    TaskDetailAPIView,
    SubtaskCollectionAPIView,
    SubtaskDetailAPIView,
)

urlpatterns = [
    # Dashboard (FBVs)
    path('dashboard/summary/', dashboard_summary, name='dashboard-summary'),
    path('dashboard/today/', today_tasks, name='today-tasks'),
    
    # Categories
    path('categories/', CategoryCollectionAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    
    # Tasks
    path('tasks/', TaskCollectionAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    
    # Subtasks
    path('tasks/<int:task_id>/subtasks/', SubtaskCollectionAPIView.as_view(), name='subtask-list'),
    path('subtasks/<int:pk>/', SubtaskDetailAPIView.as_view(), name='subtask-detail'),
]