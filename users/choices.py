from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Gender(TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("female")
    OTHER = "other", _("other")
