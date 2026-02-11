from django.contrib.auth.models import User
from django.db import models

class SailorUser(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    rank = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.PositiveBigIntegerField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(blank=True,null=True)
    otp_created_at = models.DateField(blank=True,null=True)
    is_google_auth =  models.BooleanField(default=False)
    

    def __str__(self):
        return self.name if self.name else self.email.email
