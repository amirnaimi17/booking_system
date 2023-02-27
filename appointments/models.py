import datetime
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from appointments.choices import Status
from common.utils import get_working_days, get_working_hours_in_seconds
from common.validators import DateTimeValidator
from health_providers.models import HealthProvider
from users.models import Patient, Surgeon


def validate_slots_compatibility(value):
    duration = settings.DURATION
    minutes = value.seconds / 60
    if minutes % duration != 0 or not minutes:
        raise ValidationError(
            _(
                "The duration has to be divisible by the duration " "({} minutes)."
            ).format(duration)
        )


class SurgeonAvailabilitySlot(models.Model):
    """Indicate availability of a surgeon in hospital or clinic.

    After save, Appointments will be created for patients to apply.
    """

    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE, db_index=True)
    health_provider = models.ForeignKey(
        HealthProvider, on_delete=models.CASCADE, db_index=True
    )
    start_datetime = models.DateTimeField(
        _("Available from"),
        validators=[DateTimeValidator()],
    )
    end_datetime = models.DateTimeField(
        _("To"),
        validators=[DateTimeValidator()],
    )
    visit_duration = models.DurationField(
        _("visit duration"),
        help_text="HH:MM:SS",
        validators=[
            validate_slots_compatibility,
        ],
        default=timedelta(minutes=settings.DURATION),
    )

    class Meta(TimeStampedModel.Meta):
        verbose_name = _("Surgeon Appointment Availability Slot")
        verbose_name_plural = _("Surgeon Appointment Availability Slots")

    def __str__(self):
        return f"{self.surgeon.user.get_full_name()} - {self.health_provider} - {self.start_datetime}"

    def clean(self):
        """Validate that the start datetime is before end datetime.

        It also makes sure date time range meets visit duration
        """
        if self.start_datetime > self.end_datetime:
            raise ValidationError(_("Start datetime must be before end datetime."))

        working_in_seconds = get_working_hours_in_seconds(
            self.start_datetime, self.end_datetime
        )
        if working_in_seconds < self.visit_duration.total_seconds():
            raise ValidationError(
                _("Duration specified should be longer than visit duration")
            )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        # Create Appointments from Surgeon Availability
        with transaction.atomic():
            super().save(
                force_insert=False, force_update=False, using=None, update_fields=None
            )
            working_days = get_working_days(
                start_datetime=self.start_datetime, end_datetime=self.end_datetime
            )
            visit_duration_in_minutes = self.visit_duration.total_seconds() / 60

            for working_day in working_days:
                # TODO we should create appointments based on exact date and time specified instead of start end time.
                start_time = make_aware(
                    datetime.datetime(
                        working_day.year,
                        working_day.month,
                        working_day.day,
                        settings.VISIT_START_TIME,
                    )
                )
                end_time = make_aware(
                    datetime.datetime(
                        working_day.year,
                        working_day.month,
                        working_day.day,
                        # if visit range is between 9 - 15 then last visit start date should be an hour before
                        settings.VISIT_END_TIME - 1,
                    )
                )
                while end_time >= start_time:
                    visit_end_datetime = start_time + relativedelta(
                        minutes=visit_duration_in_minutes
                    )
                    Appointment.objects.create(
                        appointment_slot=self,
                        start_datetime=start_time,
                        end_datetime=visit_end_datetime,
                    )
                    start_time += relativedelta(
                        minutes=visit_duration_in_minutes
                        + settings.BREAK_BETWEEN_APPOINTMENTS
                    )


class Appointment(TimeStampedModel):
    appointment_slot = models.ForeignKey(
        SurgeonAvailabilitySlot, on_delete=models.CASCADE
    )
    start_datetime = models.DateTimeField(
        _("Start time"),
    )
    end_datetime = models.DateTimeField(
        _("End time"),
    )
    status = models.CharField(
        _("status"), max_length=20, choices=Status.choices, default=Status.PENDING
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.appointment_slot.surgeon} - {self.appointment_slot.health_provider} - {self.appointment_slot.start_datetime.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")
