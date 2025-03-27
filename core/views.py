from django.shortcuts import render
from service_requests.models import ServiceRequest, ServiceRequestType

def home(request):
    # Different view based on user type
    context = {
        'request_types': ServiceRequestType.objects.all()[:5],
    }
    
    if request.user.is_authenticated:
        if request.user.is_customer:
            # Customer view
            context['recent_requests'] = ServiceRequest.objects.filter(
                customer=request.user.customer_profile
            ).order_by('-created_at')[:3]
        elif request.user.is_staff_member:
            # CSR view
            context['pending_requests'] = ServiceRequest.objects.filter(
                status='pending'
            ).order_by('-created_at')[:5]
    
    return render(request, 'core/home.html', context)