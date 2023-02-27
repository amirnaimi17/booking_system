from django.db import models
from django_extensions.db.models import TimeStampedModel

from users.models.mixins import PersonMixin


class Surgeon(PersonMixin, TimeStampedModel):
    specialty = models.CharField(max_length=100, null=True, blank=True)
    license_number = models.CharField(max_length=20, null=True, blank=True)
    health_providers = models.ManyToManyField(
        "health_providers.HealthProvider", related_name="surgeons"
    )

    def __str__(self):
        return self.user.get_full_name()


class Patient(PersonMixin, TimeStampedModel):
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    insurance_provider = models.CharField(max_length=100, null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)
    current_medications = models.TextField(null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    preferred_language = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()
