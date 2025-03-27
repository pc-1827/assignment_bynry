from django import forms
from service_requests.models import ServiceRequest
from accounts.models import CSRProfile

class RequestUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['status', 'priority', 'assigned_to']
    
    def __init__(self, *args, **kwargs):
        super(RequestUpdateForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = CSRProfile.objects.all()
        self.fields['assigned_to'].label_from_instance = lambda obj: f"{obj.user.get_full_name()} ({obj.employee_id})"