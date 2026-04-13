from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AuthLoginAPIView, AuthLogoutAPIView, ProfileMeAPIView

urlpatterns = [
    path('login/', AuthLoginAPIView.as_view(), name='auth-login'),
    path('logout/', AuthLogoutAPIView.as_view(), name='auth-logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/me/', ProfileMeAPIView.as_view(), name='profile-me'),
]