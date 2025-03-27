from django.contrib import admin
from .models import ServiceRequestType, ServiceRequest, RequestAttachment, RequestComment

@admin.register(ServiceRequestType)
class ServiceRequestTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'estimated_completion_days')
    search_fields = ('name',)

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'request_type', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'request_type')
    search_fields = ('title', 'description', 'customer__user__username')
    date_hierarchy = 'created_at'

@admin.register(RequestAttachment)
class RequestAttachmentAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)

@admin.register(RequestComment)
class RequestCommentAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username')
