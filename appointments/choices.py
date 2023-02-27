from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Status(TextChoices):
    """Different Statuses.

    PENDING   --> default value when appointment get created.
    REQUESTED --> when patient requests and appointment
    CONFIRMED --> when surgeon confirms the appointment
    REJECTED  --> when appointment gets rejected by surgeon
    """

    PENDING = "pending", _("pending")
    REQUESTED = "requested", _("requested")
    CONFIRMED = "confirmed", _("confirmed")
    REJECTED = "rejected", _("rejected")
