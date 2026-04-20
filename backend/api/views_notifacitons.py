from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer

@api_view(['GET'])
def notification_list(request):
    """GET /api/notifications/ — fetch all notifications for request.user."""
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    return Response(NotificationSerializer(notifications, many=True).data)

@api_view(['PATCH'])
def notification_clear(request, pk):
    """PATCH /api/notifications/<pk>/ — mark escalation notification as read."""
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
    except Notification.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    notification.is_read = True
    notification.save(update_fields=['is_read'])
    return Response(NotificationSerializer(notification).data)
