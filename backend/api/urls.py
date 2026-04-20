from django.urls import path

from .views_auth import login_view, logout_view
from .views_tasks import MedicalTaskListCreateView, MedicalTaskDetailView
from .views_symptoms import symptom_search, symptom_list_create
from .views_labs import LabReportListCreateView, LabReportDetailView
from .views_notifications import notification_list, notification_clear
from .views_profile import ProfileView
from .views_reports import generate_pdf_report

urlpatterns = [
    # Auth (FBV)
    path('auth/login/',  login_view,  name='login'),
    path('auth/logout/', logout_view, name='logout'),

    # Profile (CBV)
    path('profile/me/', ProfileView.as_view(), name='profile'),

    # Tasks (CBV — full CRUD)
    path('tasks/',      MedicalTaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', MedicalTaskDetailView.as_view(), name='task-detail'),

    # Symptoms (FBV)
    path('symptoms/search/', symptom_search,       name='symptom-search'),
    path('symptoms/',        symptom_list_create,  name='symptom-list'),

    # Labs (CBV)
    path('labs/',           LabReportListCreateView.as_view(), name='lab-list'),
    path('labs/<int:pk>/', LabReportDetailView.as_view(),     name='lab-detail'),

    # Notifications (FBV)
    path('notifications/',          notification_list,   name='notification-list'),
    path('notifications/<int:pk>/', notification_clear,  name='notification-clear'),

    # Reports (FBV)
    path('reports/summary/pdf/', generate_pdf_report, name='report-pdf'),
]
