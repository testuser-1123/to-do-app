from io import BytesIO
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import MedicalTask, SymptomEntry, LabReport
from .serializers import ReportRequestSerializer


@api_view(['GET'])
def generate_pdf_report(request):
    """
    GET /api/reports/summary/pdf/?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD
    Returns a basic PDF summary using reportlab (gracefully degrades if not installed).
    """
    serializer = ReportRequestSerializer(data=request.query_params)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    from_date = serializer.validated_data['from_date']
    to_date = serializer.validated_data['to_date']
    user = request.user

    tasks = MedicalTask.objects.filter(user=user, created_at__date__range=(from_date, to_date))
    symptoms = SymptomEntry.objects.filter(user=user, recorded_at__date__range=(from_date, to_date))
    labs = LabReport.objects.filter(user=user, uploaded_at__date__range=(from_date, to_date))

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = [
            Paragraph(f'Medical Summary: {from_date} to {to_date}', styles['Title']),
            Spacer(1, 12),
            Paragraph(f'Patient: {user.get_full_name() or user.username}', styles['Normal']),
            Spacer(1, 12),
            Paragraph(f'Tasks ({tasks.count()})', styles['Heading2']),
        ]
        for t in tasks:
            story.append(Paragraph(f'• {t.title} — {"Done" if t.is_done else "Pending"}', styles['Normal']))

        story += [
            Spacer(1, 12),
            Paragraph(f'Symptoms ({symptoms.count()})', styles['Heading2']),
        ]
        for s in symptoms:
            story.append(Paragraph(f'• {s.name} (severity {s.severity})', styles['Normal']))

        story += [
            Spacer(1, 12),
            Paragraph(f'Lab Reports ({labs.count()})', styles['Heading2']),
        ]
        for lab in labs:
            story.append(Paragraph(
                f'• Uploaded {lab.uploaded_at.date()} — {"Verified" if lab.is_verified else "Pending conclusion"}',
                styles['Normal']
            ))

        doc.build(story)
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{from_date}_{to_date}.pdf"'
        return response

    except ImportError:
        # Fallback plain-text response if reportlab not installed
        lines = [
            f'Medical Summary: {from_date} to {to_date}',
            f'Patient: {user.get_full_name() or user.username}',
            '',
            f'Tasks ({tasks.count()}):',
            *[f'  - {t.title} ({"Done" if t.is_done else "Pending"})' for t in tasks],
            '',
            f'Symptoms ({symptoms.count()}):',
            *[f'  - {s.name} severity={s.severity}' for s in symptoms],
            '',
            f'Lab Reports ({labs.count()}):',
            *[f'  - {lab.uploaded_at.date()} verified={lab.is_verified}' for lab in labs],
        ]
        return HttpResponse('\n'.join(lines), content_type='text/plain')
