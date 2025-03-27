from django.db import models
from django.conf import settings
from service_requests.models import ServiceRequest

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('request_status', 'Request Status Update'),
        ('new_comment', 'New Comment'),
        ('assigned', 'Request Assigned'),
        ('system', 'System Notification'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} for {self.user.username}"

class EmailLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='email_logs')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Email to {self.user.email} - {self.subject}"
