## Booking System

This app is a booking system designed to make it easy for patients and surgeons to schedule appointments.
The system includes Surgeon, Patient, and Health Provider entities, and it works by allowing surgeons to specify a date and time range for their visits with patients.
Once this information is entered, the app automatically creates a list of available appointments for patients to choose from.
Patients can then select the appointment that best fits their schedule and request it through the app.


IMHO there is room for improvement. For example, I was going to incorporate additional features such as email appointment confirmations and a more user-friendly interface for both doctors and patients.

Here are the list of tasks of the case study

### Patient

- request an appointment

    - Appointments can only be requested during the surgeon’s working hours (from Monday to Saturday between 9:00-15:00 local time).

    - A Patient can only book a single appointment per day with a surgeon.

    - No two booked appointments with a single surgeon can overlap (to avoid scheduling conflicts)

    - Cancel a booked appointment

    - List of future booked appointments

### Surgeon

- List of future pending appointments (only surgeon can see it).
- List of future booked appointments (only surgeon can see it)
- List of vacant appointments per day
- Confirm an appointment request
- Cancel a booked appointment

### SurgeonAvailabilitySlot

- Through this model surgeon specifies time range of the appointment in a hospital or clinic


# How to run application
> pip install -r requirements_dev.txt

> python manage.py runserver

# How to run pytest

> pytest
