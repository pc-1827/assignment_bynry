from django import forms
from .models import ServiceRequest, RequestAttachment, RequestComment

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['request_type', 'title', 'description', 'priority']
        
    def __init__(self, *args, **kwargs):
        super(ServiceRequestForm, self).__init__(*args, **kwargs)
        self.fields['request_type'].empty_label = "Select Request Type"

class RequestAttachmentForm(forms.ModelForm):
    class Meta:
        model = RequestAttachment
        fields = ['file', 'description']

class RequestCommentForm(forms.ModelForm):
    class Meta:
        model = RequestComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }