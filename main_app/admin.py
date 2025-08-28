from django.contrib import admin
from .models import DetectionResult, UserActivity

@admin.register(DetectionResult)
class DetectionResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'detection_type', 'result', 'confidence_score', 'created_at')
    list_filter = ('detection_type', 'result', 'created_at')
    search_fields = ('user__username', 'user__email', 'input_data')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'ip_address', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
