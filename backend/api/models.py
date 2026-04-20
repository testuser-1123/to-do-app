from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """FK → User (1-to-1). Stores UI preferences."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    brain_fog_mode = models.BooleanField(default=False)
    xp_points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Profile({self.user.username})'


class MedicalTask(models.Model):
    """FK → User. Full CRUD target."""
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    consequence_text = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    current_stock = models.PositiveIntegerField(default=0)
    is_done = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SymptomEntry(models.Model):
    """FK → User. Also FK → MedicalTask (optional association)."""
    SEVERITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='symptoms')
    task = models.ForeignKey(
        MedicalTask, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='symptoms'
    )  # FK relationship #2
    name = models.CharField(max_length=255)
    severity = models.PositiveSmallIntegerField(choices=SEVERITY_CHOICES, default=5)
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} (severity {self.severity})'


class LabReport(models.Model):
    """FK → User. Covers file upload + conclusion workflow."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lab_reports')
    file = models.FileField(upload_to='labs/')
    transcribed_conclusion = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'LabReport({self.user.username}, {self.uploaded_at.date()})'


class Notification(models.Model):
    """FK → User. Supports polling + clear workflow."""
    LEVEL_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('escalation', 'Escalation'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='info')
    is_read = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.level}] {self.message[:40]}'
