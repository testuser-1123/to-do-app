from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile, MedicalTask, SymptomEntry, LabReport, Notification

class LoginSerializer(serializers.Serializer):
    """Validates credentials; returns JWT tokens."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid username or password.')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
        }


class LogoutSerializer(serializers.Serializer):
    """Accepts a refresh token and blacklists it."""
    refresh = serializers.CharField()

    def validate_refresh(self, value):
        try:
            token = RefreshToken(value)
            token.blacklist()
        except Exception:
            raise serializers.ValidationError('Token is invalid or already blacklisted.')
        return value


class SymptomSearchSerializer(serializers.Serializer):
    """Query parameters for symptom search."""
    query = serializers.CharField(min_length=2, max_length=100)

    def validate_query(self, value):
        return value.strip()


class ReportRequestSerializer(serializers.Serializer):
    """Date range for PDF report generation."""
    from_date = serializers.DateField()
    to_date = serializers.DateField()

    def validate(self, data):
        if data['from_date'] > data['to_date']:
            raise serializers.ValidationError('from_date must be before to_date.')
        return data


# ── Model Serializers ─────────────────────────────────────────────────────────

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'brain_fog_mode', 'xp_points', 'created_at']
        read_only_fields = ['id', 'xp_points', 'created_at']


class MedicalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalTask
        fields = [
            'id', 'title', 'consequence_text', 'due_date',
            'valid_until', 'current_stock', 'is_done', 'priority', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class SymptomEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomEntry
        fields = ['id', 'task', 'name', 'severity', 'notes', 'recorded_at']
        read_only_fields = ['id', 'recorded_at']


class LabReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabReport
        fields = [
            'id', 'file', 'transcribed_conclusion',
            'is_verified', 'uploaded_at', 'updated_at',
        ]
        read_only_fields = ['id', 'is_verified', 'uploaded_at', 'updated_at']


class NotificationSerializer(serializers.ModelSerializer):
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'message', 'level', 'is_read', 'expires_at', 'created_at', 'is_expired']
        read_only_fields = ['id', 'message', 'level', 'expires_at', 'created_at']

    def get_is_expired(self, obj):
        if obj.expires_at is None:
            return False
        return timezone.now() > obj.expires_at
