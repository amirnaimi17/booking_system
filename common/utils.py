from dateutil import rrule
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def get_working_days(start_datetime=None, end_datetime=None):
    if not start_datetime or not end_datetime:
        raise ValidationError(_("Start and end date should be specified."))

    # Working days between start and end dates
    working_days = list(
        rrule.rrule(
            rrule.DAILY,
            dtstart=start_datetime,
            until=end_datetime,
            byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR),
        )
    )
    return working_days


def get_working_hours(start_datetime=None, end_datetime=None):
    working_days = get_working_days(start_datetime, end_datetime)

    if not working_days:
        raise ValidationError(_("The date is holiday."))

    # Working hours if start and end date are in the same day
    if len(working_days) == 1:
        working_days = rrule.rrule(
            rrule.DAILY, byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR)
        )
        # Check date is not holiday
        if start_datetime.weekday() in working_days._byweekday:
            time_difference_seconds = (end_datetime - start_datetime).total_seconds()
            # Calculate the time difference in hours and minutes
            hours, remainder = divmod(time_difference_seconds, 3600)
            return hours, remainder

    # Total working hours
    return len(working_days) * settings.WORKING_HOURS_PER_DAY, 0


def get_working_hours_in_seconds(start_datetime=None, end_datetime=None):
    working_hours, remainder = get_working_hours(start_datetime, end_datetime)

    if remainder:
        minutes, seconds = divmod(remainder, 60)
        return working_hours * 300 + (minutes * 60) + seconds

    return working_hours * 60 * 60
