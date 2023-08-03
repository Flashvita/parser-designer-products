from account.models import User
from rest_framework import serializers

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    grecaptcha_token = serializers.CharField(required=True)
