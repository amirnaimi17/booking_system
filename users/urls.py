from django.urls import path

from users.views import PatientSignUpView, SurgeonSignupView

urlpatterns = [
    path("signup/patient/", PatientSignUpView.as_view(), name="patient_signup"),
    path("signup/surgeon/", SurgeonSignupView.as_view(), name="surgeon_signup"),
]
