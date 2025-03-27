from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from service_requests.models import ServiceRequest
from service_requests.forms import RequestCommentForm
from notifications.utils import send_status_update_notification
from .forms import RequestUpdateForm

@login_required
def dashboard(request):
    if not request.user.is_staff_member:
        messages.error(request, "Access denied. This area is for staff only.")
        return redirect('home')
    
    # Get request statistics
    pending_count = ServiceRequest.objects.filter(status='pending').count()
    in_progress_count = ServiceRequest.objects.filter(status='in_progress').count()
    completed_count = ServiceRequest.objects.filter(status='completed').count()
    
    # Get recent/urgent requests
    recent_urgent = ServiceRequest.objects.filter(
        Q(priority='urgent') | Q(priority='high')
    ).order_by('-created_at')[:5]
    
    # Requests assigned to this CSR
    if hasattr(request.user, 'csr_profile'):
        assigned_requests = ServiceRequest.objects.filter(
            assigned_to=request.user.csr_profile
        ).order_by('-created_at')[:5]
    else:
        assigned_requests = []
    
    context = {
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'recent_urgent': recent_urgent,
        'assigned_requests': assigned_requests
    }
    
    return render(request, 'csr_dashboard/dashboard.html', context)

@login_required
def request_list(request):
    if not request.user.is_staff_member:
        messages.error(request, "Access denied. This area is for staff only.")
        return redirect('home')
    
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    
    requests = ServiceRequest.objects.all().order_by('-created_at')
    
    if status_filter and status_filter != 'all':
        requests = requests.filter(status=status_filter)
        
    if priority_filter and priority_filter != 'all':
        requests = requests.filter(priority=priority_filter)
    
    return render(request, 'csr_dashboard/request_list.html', {
        'requests': requests,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    })

@login_required
def request_detail(request, pk):
    if not request.user.is_staff_member:
        messages.error(request, "Access denied. This area is for staff only.")
        return redirect('home')
    
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    comments = service_request.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = RequestUpdateForm(request.POST, instance=service_request)
        if form.is_valid():
            old_status = service_request.status
            updated_request = form.save()
            
            # If status changed, send notification
            if old_status != updated_request.status:
                send_status_update_notification(service_request)
            
            messages.success(request, "Request has been updated successfully.")
            return redirect('csr_request_detail', pk=service_request.pk)
    else:
        form = RequestUpdateForm(instance=service_request)
    
    comment_form = RequestCommentForm()
    
    return render(request, 'csr_dashboard/request_detail.html', {
        'service_request': service_request,
        'comments': comments,
        'form': form,
        'comment_form': comment_form
    })