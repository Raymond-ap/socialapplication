from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
