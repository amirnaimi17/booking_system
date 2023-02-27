from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Patient, Surgeon


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = "__all__"


class SurgeonSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Surgeon
        fields = "__all__"
