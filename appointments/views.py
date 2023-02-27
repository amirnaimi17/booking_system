from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, UpdateAPIView

from appointments.choices import Status
from appointments.models import Appointment
from appointments.serializers import (
    AppointmentCancelSerializer,
    AppointmentCancelSurgeonSerializer,
    AppointmentConfirmSerializer,
    AppointmentRequestSerializer,
    AppointmentSerializer,
)
from common.permissions import IsPatientAuthenticated, IsSurgeonAuthenticated


class RequestAppointmentView(UpdateAPIView):
    queryset = Appointment.objects.select_related(
        "patient",
        "appointment_slot",
    ).all()
    serializer_class = AppointmentRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsPatientAuthenticated]
    lookup_field = "id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_serializer(self, *args, **kwargs):
        """Provide Serializer for Patch Update."""
        kwargs["data"] = {
            "status": Status.REQUESTED,
            "patient": self.request.user.patient.pk,
        }
        return super().get_serializer(*args, **kwargs)


class CancelAppointmentPatientView(UpdateAPIView):
    queryset = Appointment.objects.select_related(
        "patient",
    ).all()
    serializer_class = AppointmentCancelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsPatientAuthenticated]
    lookup_field = "id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_serializer(self, *args, **kwargs):
        """Provide Serializer for Patch Update."""
        kwargs["data"] = {"status": Status.PENDING, "patient": None}
        return super().get_serializer(*args, **kwargs)


class ListAppointmentPatientView(ListAPIView):
    queryset = Appointment.objects.select_related(
        "patient",
        "appointment_slot",
        "appointment_slot__surgeon",
        "appointment_slot__health_provider",
    ).all()
    serializer_class = AppointmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsPatientAuthenticated]

    def get_queryset(self):
        now = timezone.now()
        return self.queryset.filter(
            patient=self.request.user.patient,
            status=Status.CONFIRMED,
            start_datetime__gte=now,
        )


class ListConfirmedAppointmentSurgeonView(ListAPIView):
    queryset = Appointment.objects.select_related(
        "appointment_slot",
        "appointment_slot__surgeon",
    ).all()
    serializer_class = AppointmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSurgeonAuthenticated]

    def get_queryset(self):
        now = timezone.now()
        return self.queryset.filter(
            appointment_slot__surgeon=self.request.user.surgeon,
            status=Status.CONFIRMED,
            start_datetime__gte=now,
        )


class ListPendingAppointmentPatientView(ListAPIView):
    queryset = Appointment.objects.select_related(
        "appointment_slot",
        "appointment_slot__surgeon",
    ).all()
    serializer_class = AppointmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSurgeonAuthenticated]

    def get_queryset(self):
        now = timezone.now()
        return self.queryset.filter(
            appointment_slot__surgeon=self.request.user.surgeon,
            status=Status.PENDING,
            start_datetime__gte=now,
        )


class ListRequestedAppointmentPatientView(ListAPIView):
    queryset = Appointment.objects.select_related(
        "appointment_slot",
        "appointment_slot__surgeon",
    ).all()
    serializer_class = AppointmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSurgeonAuthenticated]

    def get_queryset(self):
        now = timezone.now()
        return self.queryset.filter(
            appointment_slot__surgeon=self.request.user.surgeon,
            status=Status.REQUESTED,
            start_datetime__gte=now,
        )


class CancelAppointmentSurgeonView(UpdateAPIView):
    queryset = Appointment.objects.select_related(
        "appointment_slot", "appointment_slot__surgeon"
    ).all()
    serializer_class = AppointmentCancelSurgeonSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSurgeonAuthenticated]
    lookup_field = "id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_serializer(self, *args, **kwargs):
        """Provide Serializer for Patch Update."""
        kwargs["data"] = {"status": Status.PENDING, "patient": None}
        return super().get_serializer(*args, **kwargs)


class ConfirmAppointmentView(UpdateAPIView):
    queryset = Appointment.objects.select_related(
        "appointment_slot", "appointment_slot__surgeon"
    ).all()
    serializer_class = AppointmentConfirmSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSurgeonAuthenticated]
    lookup_field = "id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_serializer(self, *args, **kwargs):
        """Provide Serializer for Patch Update."""
        kwargs["data"] = {
            "status": Status.CONFIRMED,
        }
        return super().get_serializer(*args, **kwargs)
