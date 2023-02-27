from django.urls import path

from appointments.views import (
    CancelAppointmentPatientView,
    CancelAppointmentSurgeonView,
    ConfirmAppointmentView,
    ListAppointmentPatientView,
    ListConfirmedAppointmentSurgeonView,
    ListPendingAppointmentPatientView,
    ListRequestedAppointmentPatientView,
    RequestAppointmentView,
)

urlpatterns = [
    path(
        "request/<int:id>/",
        RequestAppointmentView.as_view(),
        name="request_appointment",
    ),
    path(
        "cancel/<int:id>/",
        CancelAppointmentPatientView.as_view(),
        name="cancel_appointment",
    ),
    path("list", ListAppointmentPatientView.as_view(), name="list_appointments"),
    # list of appointments for surgeon
    path(
        "list/confirmed",
        ListConfirmedAppointmentSurgeonView.as_view(),
        name="list_appointments_confirmed",
    ),
    path(
        "list/pending",
        ListPendingAppointmentPatientView.as_view(),
        name="list_appointments_pending",
    ),
    path(
        "list/requested",
        ListRequestedAppointmentPatientView.as_view(),
        name="list_appointments_requested",
    ),
    path(
        "cancel/<int:id>/surgeon",
        CancelAppointmentSurgeonView.as_view(),
        name="cancel_appointment_by_surgeon",
    ),
    path(
        "confirm/<int:id>/",
        ConfirmAppointmentView.as_view(),
        name="confirm_appointment",
    ),
]
