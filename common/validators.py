from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class DateTimeValidator(BaseValidator):
    message = _("The date you enter must be in the future" " It is %(show_value)s.")
    code = "date_validation"

    def __init__(self, limit_value=timezone.timedelta(days=1), message=None):
        super().__init__(limit_value=limit_value, message=message)

    def __call__(self, value):
        now = timezone.now() - timezone.timedelta(minutes=2)

        if self.compare(value, now):
            params = {
                "show_value": value.isoformat(),
            }
            raise ValidationError(self.message, code=self.code, params=params)

    def compare(self, value, now):
        return value <= now
