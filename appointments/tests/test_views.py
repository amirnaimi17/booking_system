from datetime import timedelta

from django.utils import timezone
from freezegun import freeze_time
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from appointments.choices import Status
from appointments.models import Appointment


class TestRequestAppointmentView:
    def create_appointments(self, surgeon, health_provider):
        now = timezone.now()
        baker.make_recipe(
            "appointments.SurgeonAvailabilitySlot",
            start_datetime=now,
            end_datetime=now + timedelta(days=1),
            surgeon=surgeon,
            health_provider=health_provider,
        )

    @freeze_time("2023-02-27 12:00:00")
    def test_patch_api_view(self, patient, token, surgeon, health_provider):
        assert not Appointment.objects.all()
        self.create_appointments(surgeon, health_provider)
        assert Appointment.objects.all()

        appointment = Appointment.objects.last()
        assert appointment.status == Status.PENDING
        assert not appointment.patient

        client = APIClient()
        # Add the token to the client credentials
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        patch_url = reverse("request_appointment", kwargs={"id": appointment.pk})
        response = client.patch(patch_url)
        assert response.status_code == 200
        appointment.refresh_from_db()

        assert appointment.status == Status.REQUESTED
        assert appointment.patient == patient

    @freeze_time("2023-02-27 18:00:00")
    def test_invalid_time_patch_api_view(
        self, patient, token, surgeon, health_provider
    ):
        assert not Appointment.objects.all()
        self.create_appointments(surgeon, health_provider)
        assert Appointment.objects.all()

        appointment = Appointment.objects.last()
        assert appointment.status == Status.PENDING
        assert not appointment.patient

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        patch_url = reverse("request_appointment", kwargs={"id": appointment.pk})
        response = client.patch(patch_url)
        assert response.status_code == 400
        assert response.json()["error"] == [
            "Appointment should be made during working hours."
        ]

        assert appointment.status == Status.PENDING
        assert appointment.patient is None

    @freeze_time("2023-02-27 12:00:00")
    def test_invalid_status_patch_api_view(
        self, patient, token, surgeon, health_provider
    ):
        assert not Appointment.objects.all()
        self.create_appointments(surgeon, health_provider)
        assert Appointment.objects.all()

        appointment = Appointment.objects.last()
        appointment.status = Status.CONFIRMED
        appointment.patient = patient
        appointment.save()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        patch_url = reverse("request_appointment", kwargs={"id": appointment.pk})
        response = client.patch(patch_url)
        assert response.status_code == 400
        assert response.json()["status"] == ["Only pending status can be requested."]


# TODO implement test for other views as well.
