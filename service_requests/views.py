from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServiceRequest
from .forms import RequestCommentForm
from notifications.utils import send_comment_notification  

@login_required
def service_request_detail(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    
    # Check permissions
    is_owner = request.user.is_customer and hasattr(request.user, 'customer_profile') and service_request.customer == request.user.customer_profile
    is_staff = request.user.is_staff_member
    
    if not (is_owner or is_staff):
        messages.error(request, "You don't have permission to view this service request.")
        return redirect('home')
    
    comments = service_request.comments.all().order_by('-created_at')
    comment_form = RequestCommentForm()
    
    return render(request, 'service_requests/detail.html', {
        'service_request': service_request,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def add_comment(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    
    # Check permissions
    is_owner = request.user.is_customer and hasattr(request.user, 'customer_profile') and service_request.customer == request.user.customer_profile
    is_staff = request.user.is_staff_member
    
    if not (is_owner or is_staff):
        messages.error(request, "You don't have permission to comment on this service request.")
        return redirect('home')
    
    if request.method == 'POST':
        form = RequestCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.service_request = service_request
            comment.user = request.user
            comment.save()
            
            # Send notification for the new comment
            send_comment_notification(comment)
            
            messages.success(request, "Your comment has been added.")
    
    return redirect('service_request_detail', pk=service_request.pk)
