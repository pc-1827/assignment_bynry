from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from service_requests.models import ServiceRequest, RequestAttachment
from service_requests.forms import ServiceRequestForm, RequestAttachmentForm
from accounts.models import CustomerProfile

@login_required
def dashboard(request):
    if not request.user.is_customer:
        messages.error(request, "Access denied. This area is for customers only.")
        return redirect('home')
    
    # Get customer profile or create if doesn't exist
    customer_profile, created = CustomerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'account_number': f"TEMP-{request.user.id}",
            'service_address': '',
            'city': '',
            'state': '',
            'zip_code': ''
        }
    )
    
    # Get recent service requests
    recent_requests = ServiceRequest.objects.filter(
        customer=customer_profile
    ).order_by('-created_at')[:5]
    
    # Count requests by status
    pending_count = ServiceRequest.objects.filter(customer=customer_profile, status='pending').count()
    in_progress_count = ServiceRequest.objects.filter(customer=customer_profile, status='in_progress').count()
    completed_count = ServiceRequest.objects.filter(customer=customer_profile, status='completed').count()
    
    context = {
        'recent_requests': recent_requests,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
    }
    
    return render(request, 'customer_portal/dashboard.html', context)

@login_required
def request_list(request):
    if not request.user.is_customer:
        messages.error(request, "Access denied. This area is for customers only.")
        return redirect('home')
    
    status_filter = request.GET.get('status', '')
    
    customer_profile = request.user.customer_profile
    requests = ServiceRequest.objects.filter(customer=customer_profile).order_by('-created_at')
    
    if status_filter and status_filter != 'all':
        requests = requests.filter(status=status_filter)
    
    return render(request, 'customer_portal/request_list.html', {
        'requests': requests,
        'status_filter': status_filter,
    })

@login_required
def create_request(request):
    if not request.user.is_customer:
        messages.error(request, "Access denied. This area is for customers only.")
        return redirect('home')
    
    AttachmentFormSet = modelformset_factory(
        RequestAttachment,
        form=RequestAttachmentForm,
        extra=3,
        max_num=5
    )
    
    if request.method == 'POST':
        request_form = ServiceRequestForm(request.POST)
        attachment_formset = AttachmentFormSet(
            request.POST,
            request.FILES,
            queryset=RequestAttachment.objects.none()
        )
        
        if request_form.is_valid() and attachment_formset.is_valid():
            # Save request
            service_request = request_form.save(commit=False)
            service_request.customer = request.user.customer_profile
            service_request.save()
            
            # Save attachments
            attachments = attachment_formset.save(commit=False)
            for attachment in attachments:
                if attachment.file:  # Only save if file was uploaded
                    attachment.service_request = service_request
                    attachment.save()
            
            messages.success(request, "Your service request has been submitted successfully.")
            return redirect('customer_dashboard')
    else:
        request_form = ServiceRequestForm()
        attachment_formset = AttachmentFormSet(queryset=RequestAttachment.objects.none())
    
    return render(request, 'customer_portal/create_request.html', {
        'request_form': request_form,
        'attachment_formset': attachment_formset,
    })