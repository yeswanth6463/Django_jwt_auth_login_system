from rest_framework import serializers
from .models import SailorUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class SailorUserSerializer(serializers.ModelSerializer):
    email = serializers.SlugRelatedField(
        slug_field = 'email',
        queryset = User.objects.all()
    )
    class Meta:
        model = SailorUser
        fields = ['id', 'email', 'name', 'age', 'rank', 'mobile_number', 'address']