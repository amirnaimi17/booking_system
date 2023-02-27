from model_bakery.random_gen import gen_datetime
from model_bakery.recipe import Recipe, foreign_key

from health_providers.baker_recipes import HealthProvider
from users.baker_recipes import Patient, Surgeon

SurgeonAvailabilitySlot = Recipe(
    "appointments.SurgeonAvailabilitySlot",
    surgeon=foreign_key(Surgeon),
    health_provider=foreign_key(HealthProvider),
    start_datetime=gen_datetime,
    end_datetime=gen_datetime,
)

Appointment = Recipe(
    "appointments.Appointment",
    appointment_slot=foreign_key(SurgeonAvailabilitySlot),
    start_datetime=gen_datetime,
    patient=foreign_key(Patient),
)
