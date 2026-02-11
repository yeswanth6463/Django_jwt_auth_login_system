from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from django.contrib.auth.models import User
from .models import SailorUser

@receiver(user_logged_in)
def create_sailor_user(request, user, **kwargs):
    if not SailorUser.objects.filter(email=user.email).exists():
        SailorUser.objects.create(
            name=user.username or user.email,
            age=0,
            rank="",
            email=user.email,
            mobile_number="",
            address=""
        )
