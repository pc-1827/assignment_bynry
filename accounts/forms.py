from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomerProfile, CSRProfile

class CustomerSignUpForm(UserCreationForm):
    account_number = forms.CharField(max_length=20)
    service_address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=50)
    zip_code = forms.CharField(max_length=10)
    phone_number = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 
                 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
            CustomerProfile.objects.create(
                user=user,
                account_number=self.cleaned_data.get('account_number'),
                service_address=self.cleaned_data.get('service_address'),
                city=self.cleaned_data.get('city'),
                state=self.cleaned_data.get('state'),
                zip_code=self.cleaned_data.get('zip_code')
            )
        return user

class CustomerProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    phone_number = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = CustomerProfile
        fields = ['service_address', 'city', 'state', 'zip_code']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CustomerProfileUpdateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['phone_number'].initial = user.phone_number