from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission


class IsPatientAuthenticated(BasePermission):
    """Allows access only to authenticated patients."""

    def has_permission(self, request, view):
        if request.user and not hasattr(request.user, "patient"):
            raise ValidationError("User is not authorized")
        return bool(
            request.user and request.user.is_authenticated and request.user.patient
        )


class IsSurgeonAuthenticated(BasePermission):
    """Allows access only to authenticated surgeons."""

    def has_permission(self, request, view):
        if request.user and not hasattr(request.user, "surgeon"):
            raise ValidationError("User is not authorized")
        return bool(
            request.user and request.user.is_authenticated and request.user.surgeon
        )
