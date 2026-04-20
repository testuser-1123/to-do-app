from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import SymptomEntry
from .serializers import SymptomEntrySerializer, SymptomSearchSerializer


# ── FBV #3: Symptom Search ────────────────────────────────────────────────────

@api_view(['GET'])
def symptom_search(request):
    """GET /api/symptoms/search/?query=... — live search across user's symptoms."""
    serializer = SymptomSearchSerializer(data=request.query_params)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    q = serializer.validated_data['query']
    results = SymptomEntry.objects.filter(
        user=request.user, name__icontains=q
    ).order_by('-recorded_at')[:20]
    return Response(SymptomEntrySerializer(results, many=True).data)


# ── FBV #4: Symptom List / Create ─────────────────────────────────────────────

@api_view(['GET', 'POST'])
def symptom_list_create(request):
    """
    GET  /api/symptoms/ — all user symptoms
    POST /api/symptoms/ — save new symptom linked to request.user
    """
    if request.method == 'GET':
        symptoms = SymptomEntry.objects.filter(user=request.user).order_by('-recorded_at')
        return Response(SymptomEntrySerializer(symptoms, many=True).data)

    serializer = SymptomEntrySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
