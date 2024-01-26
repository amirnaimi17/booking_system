from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import PatientSerializer, SurgeonSerializer, UserSerializer


class PatientSignUpView(CreateAPIView):
    serializer_class = PatientSerializer

    def post(self, request, *args, **kwargs):
        # Validate the incoming data using the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the User object and set the password
        user = User(
            username=request.data["user.username"], email=request.data["user.email"]
        )
        user.set_password(request.data["user.password"])
        user.save()

        # Create the Surgeon object and set the user
        patient = serializer.save(user=user)

        # Create a token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Serialize the response data
        user_serializer = UserSerializer(user)
        patient_serializer = self.get_serializer(patient)
        response_data = {
            "user": user_serializer.data,
            "surgeon": patient_serializer.data,
            "token": token.key,
        }

        # Return the response
        return Response(response_data, status=status.HTTP_201_CREATED)


class SurgeonSignupView(CreateAPIView):
    serializer_class = SurgeonSerializer

    def post(self, request, *args, **kwargs):
        # Validate the incoming data using the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the User object and set the password
        user = User(
            username=request.data["user.username"], email=request.data["user.email"]
        )
        user.set_password(request.data["user.password"])
        user.save()

        # Create the Surgeon object and set the user
        surgeon = serializer.save(user=user)

        # Create a token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Serialize the response data
        user_serializer = UserSerializer(user)
        surgeon_serializer = self.get_serializer(surgeon)
        response_data = {
            "user": user_serializer.data,
            "surgeon": surgeon_serializer.data,
            "token": token.key,
        }

        # Return the response
        return Response(response_data, status=status.HTTP_201_CREATED)


def some_test_to_catch_codecov1(a):
    x = 4 + a
    return x


def some_test_to_catch_codecov2(a):
    x = 5 + a
    return x


def some_test_to_catch_codecov3(a):
    x = 6 + a
    return x
