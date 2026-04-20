from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LabReport, Notification
from .serializers import LabReportSerializer


class LabReportListCreateView(APIView):
    """
    GET  /api/labs/  — list lab reports
    POST /api/labs/  — upload a lab file; fires a system notification
    """

    def get(self, request):
        labs = LabReport.objects.filter(user=request.user).order_by('-uploaded_at')
        return Response(LabReportSerializer(labs, many=True).data)

    def post(self, request):
        serializer = LabReportSerializer(data=request.data)
        if serializer.is_valid():
            lab = serializer.save(user=request.user)
            Notification.objects.create(
                user=request.user,
                message=f'Lab report uploaded. Please fill in the conclusion for report #{lab.id}.',
                level='info',
                expires_at=timezone.now() + timezone.timedelta(days=3),
            )
            return Response(LabReportSerializer(lab).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LabReportDetailView(APIView):
    """
    GET   /api/labs/<pk>/  — retrieve
    PATCH /api/labs/<pk>/  — save conclusion; sets is_verified = True
    """

    def _get_lab(self, request, pk):
        try:
            return LabReport.objects.get(pk=pk, user=request.user)
        except LabReport.DoesNotExist:
            return None

    def get(self, request, pk):
        lab = self._get_lab(request, pk)
        if lab is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(LabReportSerializer(lab).data)

    def patch(self, request, pk):
        lab = self._get_lab(request, pk)
        if lab is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LabReportSerializer(lab, data=request.data, partial=True)
        if serializer.is_valid():
            # If a conclusion was provided, mark verified
            if 'transcribed_conclusion' in request.data and request.data['transcribed_conclusion']:
                lab = serializer.save(is_verified=True)
            else:
                lab = serializer.save()
            return Response(LabReportSerializer(lab).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
