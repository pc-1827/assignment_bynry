from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerSignUpForm, CustomerProfileUpdateForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = CustomerSignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomerProfileUpdateForm(request.POST, instance=request.user.customer_profile, user=request.user)
        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.phone_number = form.cleaned_data.get('phone_number')
            user.save()
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = CustomerProfileUpdateForm(instance=request.user.customer_profile, user=request.user)
    return render(request, 'accounts/update_profile.html', {'form': form})