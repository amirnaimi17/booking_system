from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from appointments.choices import Status
from appointments.models import Appointment, SurgeonAvailabilitySlot


class AppointmentSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurgeonAvailabilitySlot
        fields = ["surgeon", "health_provider"]


class AppointmentSerializer(serializers.ModelSerializer):
    appointment_slot = AppointmentSlotSerializer()

    class Meta:
        model = Appointment
        fields = [
            "status",
            "start_datetime",
            "appointment_slot",
        ]


class AppointmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, attrs):
        instance = self.instance
        request = self.context.get("request")
        if instance.status != Status.PENDING:
            raise serializers.ValidationError(
                {"status": _("Only pending status can be requested.")}
            )

        # Appointments can only be requested during the surgeon’s working hours
        now = timezone.localtime()
        if now.hour < settings.VISIT_START_TIME or now.hour > settings.VISIT_END_TIME:
            raise serializers.ValidationError(
                {"error": _("Appointment should be made during working hours.")}
            )

        # A Patient can only book a single appointment per day with a surgeon.
        # Appointment slot can be in multiple range dates, so it should be filtered on the exact date
        patient_already_requested = instance.appointment_slot.appointment_set.filter(
            patient=request.user.patient,
            status=Status.REQUESTED,
            appointment_slot__start_datetime__date__lte=instance.start_datetime.date(),
            appointment_slot__end_datetime__date__gte=instance.start_datetime.date(),
        )
        if patient_already_requested:
            raise serializers.ValidationError(
                f"patient already requested for an appointment on the date {instance.start_datetime.date()}"
            )

        return attrs


class AppointmentCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, attrs):
        instance = self.instance
        request = self.context.get("request")
        # That's weird that patient can only cancel booked appointment.
        if instance.status != Status.CONFIRMED:
            raise serializers.ValidationError(
                {"status": _("Appointment can not be canceled.")}
            )
        if instance.patient != request.user.patient:
            raise serializers.ValidationError(
                {"status": _("You are not allowed to cancel this appointment.")}
            )

        return attrs


class AppointmentCancelSurgeonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, attrs):
        instance = self.instance
        request = self.context.get("request")
        if instance.status != Status.CONFIRMED:
            raise serializers.ValidationError(
                {"status": _("Appointment can not be canceled.")}
            )
        if instance.appointment_slot.surgeon != request.user.surgeon:
            raise serializers.ValidationError(
                {"status": _("You are not allowed to cancel this appointment.")}
            )

        return attrs


class AppointmentConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, attrs):
        instance = self.instance
        request = self.context.get("request")
        if instance.status == Status.CONFIRMED:
            raise serializers.ValidationError(
                {"status": _("This is already confirmed.")}
            )
        if instance.status != Status.REQUESTED:
            raise serializers.ValidationError(
                {"status": _("Only Requested status can be confirmed.")}
            )
        if instance.appointment_slot.surgeon != request.user.surgeon:
            raise serializers.ValidationError(
                {"status": _("You are not allowed to confirm this appointment.")}
            )

        return attrs
