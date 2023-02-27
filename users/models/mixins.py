from django.contrib.auth.models import User
from django.db import models, transaction

from users.choices import Gender


class PersonMixin(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=Gender.choices)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.id and not self.user:
                self.user = User.objects.create(
                    username=self.email, email=self.email, first_name=self.fi
                )
            super().save(*args, **kwargs)

    class Meta:
        abstract = True

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        return f"{self.user.first_name} {self.user.last_name}"
