from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Notification, EmailLog

def create_notification(user, notification_type, text, service_request=None):
    """Create a new notification for a user"""
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        text=text,
        service_request=service_request
    )

def send_email_notification(user, subject, template, context=None):
    """Send an email notification"""
    if context is None:
        context = {}
    
    html_message = render_to_string(template, context)
    
    success = True
    try:
        send_mail(
            subject=subject,
            message='',  # Plain text version
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )
    except Exception as e:
        success = False
        print(f"Error sending email: {str(e)}")
    
    # Log the email
    EmailLog.objects.create(
        user=user,
        subject=subject,
        body=html_message,
        success=success
    )
    
    return success

def send_status_update_notification(service_request):
    """Send notification when service request status changes"""
    customer = service_request.customer.user
    
    # Create in-app notification
    create_notification(
        user=customer,
        notification_type='request_status',
        text=f"Your service request '{service_request.title}' status has been updated to {service_request.get_status_display()}.",
        service_request=service_request
    )
    
    # Send email notification
    send_email_notification(
        user=customer,
        subject=f"Service Request Status Updated - {service_request.title}",
        template='notifications/email/status_update.html',
        context={'service_request': service_request, 'site_domain': 'localhost:8000'} 
    )

def send_comment_notification(comment):
    """Send notification when a new comment is added"""
    service_request = comment.service_request
    
    # Determine recipient (if CSR commented, notify customer and vice versa)
    if comment.user.is_staff_member:
        # Staff commented, notify customer
        recipient = service_request.customer.user
        notification_text = f"A customer service representative has commented on your request '{service_request.title}'."
        
        # Create in-app notification
        create_notification(
            user=recipient,
            notification_type='new_comment',
            text=notification_text,
            service_request=service_request
        )
        
        # Send email notification
        send_email_notification(
            user=recipient,
            subject=f"New Comment on Your Service Request - {service_request.title}",
            template='notifications/email/new_comment.html',
            context={'service_request': service_request, 'comment': comment, 'site_domain': 'localhost:8000'}
        )
    else:
        # Customer commented, notify assigned CSR if available
        if service_request.assigned_to:
            recipient = service_request.assigned_to.user
            notification_text = f"Customer has commented on request '{service_request.title}'."
            
            # Create in-app notification
            create_notification(
                user=recipient,
                notification_type='new_comment',
                text=notification_text,
                service_request=service_request
            )
            
            # Send email notification
            send_email_notification(
                user=recipient,
                subject=f"Customer Comment on Service Request #{service_request.id}",
                template='notifications/email/new_comment.html',
                context={'service_request': service_request, 'comment': comment, 'site_domain': 'localhost:8000'}
            )