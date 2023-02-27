from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from freezegun import freeze_time
from model_bakery import baker

from appointments.models import Appointment


class TestSurgeonAvailabilitySlot:
    @freeze_time("2023-02-27")
    def test_valid_availability(self, surgeon, health_provider, settings):
        assert not Appointment.objects.all()
        now = timezone.now()
        availability = baker.make_recipe(
            "appointments.SurgeonAvailabilitySlot",
            start_datetime=now,
            end_datetime=now + timedelta(days=1),
            surgeon=surgeon,
            health_provider=health_provider,
        )
        assert availability.visit_duration == timedelta(minutes=settings.DURATION)

        assert Appointment.objects.all()
        # Twelve appointment will be created each 45 minutes and 15 minutes break for two days
        assert Appointment.objects.count() == 12

    @freeze_time("2023-02-27")
    def test_invalid_availability(self, surgeon, health_provider, settings):
        assert not Appointment.objects.all()
        now = timezone.now()
        availability = baker.make_recipe(
            "appointments.SurgeonAvailabilitySlot",
            start_datetime=now,
            end_datetime=now,
            surgeon=surgeon,
            health_provider=health_provider,
        )
        with pytest.raises(ValidationError) as e:
            availability.clean()
        assert "Duration specified should be longer than visit duration" in e.value

    @freeze_time("2023-02-27")
    def test_invalid_availability_start_datetime(
        self, surgeon, health_provider, settings
    ):
        assert not Appointment.objects.all()
        now = timezone.now()
        availability = baker.make_recipe(
            "appointments.SurgeonAvailabilitySlot",
            start_datetime=now + timedelta(days=1),
            end_datetime=now,
            surgeon=surgeon,
            health_provider=health_provider,
        )
        with pytest.raises(ValidationError) as e:
            availability.clean()
        assert "Start datetime must be before end datetime." in e.value

    @freeze_time("2023-02-26")
    def test_do_not_create_appointment_for_holidays(
        self, surgeon, health_provider, settings
    ):
        assert not Appointment.objects.all()

        now = timezone.now()
        baker.make_recipe(
            "appointments.SurgeonAvailabilitySlot",
            start_datetime=now,
            end_datetime=now + timedelta(days=1),
            surgeon=surgeon,
            health_provider=health_provider,
        )

        assert Appointment.objects.all()
        # six appointment will be created each 45 minutes and 15 minutes break for 1 day
        # since the first day is holiday appointment will not be created
        assert Appointment.objects.count() == 6
