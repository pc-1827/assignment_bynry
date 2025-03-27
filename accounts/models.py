from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_staff_member = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.username

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    account_number = models.CharField(max_length=20, unique=True)
    service_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.user.username} - {self.account_number}"

class CSRProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='csr_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"