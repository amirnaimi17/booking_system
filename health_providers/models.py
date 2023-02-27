from django.db import models


class HealthProvider(models.Model):
    """
    A health provider that can be either clinic or hospital.

    It can be two separate entities depending on what specific requirements are needed.
    Here for simplicity I just considered as a single entity.
    """

    name = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    is_clinic = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)

    def __str__(self):
        return self.name
