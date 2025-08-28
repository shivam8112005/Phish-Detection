from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DetectionResult(models.Model):
    DETECTION_TYPES = [
        ('url', 'URL Detection'),
        ('email', 'Email Detection'),
        ('sms', 'SMS Detection'),
        ('file', 'File Analysis'),
    ]
    
    RESULT_TYPES = [
        ('safe', 'Safe'),
        ('suspicious', 'Suspicious'),
        ('dangerous', 'Dangerous'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    detection_type = models.CharField(max_length=10, choices=DETECTION_TYPES)
    input_data = models.TextField()
    result = models.CharField(max_length=10, choices=RESULT_TYPES)
    confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.detection_type} - {self.result} - {self.created_at}"

class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('detection', 'Detection Performed'),
        ('profile_update', 'Profile Updated'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'User Activities'
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.created_at}"
