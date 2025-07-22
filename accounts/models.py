from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    registration_method = models.CharField(max_length=10, choices=[
        ('email', 'Email'), 
        ('phone', 'Phone'),
        ('both', 'Both')
    ], default='email')
    
    def clean(self):
        if not self.email and not self.phone_number:
            raise ValidationError("Either email or phone number must be provided")
        
        if self.email:
            try:
                validate_email(self.email)
            except ValidationError:
                raise ValidationError("Invalid email format")
    
    def save(self, *args, **kwargs):
        self.clean()
        if self.email and self.phone_number:
            self.registration_method = 'both'
        elif self.email:
            self.registration_method = 'email'
        else:
            self.registration_method = 'phone'
        super().save(*args, **kwargs)


class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    otp_type = models.CharField(max_length=10, choices=[('email', 'Email'), ('phone', 'Phone')])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at
    
    