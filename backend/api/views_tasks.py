from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MedicalTask
from .serializers import MedicalTaskSerializer


class MedicalTaskListCreateView(APIView):
    """
    CBV #1
    GET  /api/tasks/        — list user's tasks
    POST /api/tasks/        — create a task linked to request.user
    """

    def get(self, request):
        tasks = MedicalTask.objects.filter(user=request.user).order_by('-created_at')
        serializer = MedicalTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MedicalTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)   # link to request.user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicalTaskDetailView(APIView):
    """
    CBV #2
    GET    /api/tasks/<pk>/ — retrieve
    PATCH  /api/tasks/<pk>/ — partial update (mark done, etc.)
    DELETE /api/tasks/<pk>/ — delete
    """

    def _get_task(self, request, pk):
        try:
            return MedicalTask.objects.get(pk=pk, user=request.user)
        except MedicalTask.DoesNotExist:
            return None

    def get(self, request, pk):
        task = self._get_task(request, pk)
        if task is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(MedicalTaskSerializer(task).data)

    def patch(self, request, pk):
        task = self._get_task(request, pk)
        if task is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MedicalTaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self._get_task(request, pk)
        if task is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
