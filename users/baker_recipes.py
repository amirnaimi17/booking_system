import functools

from django.contrib.auth import get_user_model
from model_bakery.random_gen import gen_string
from model_bakery.recipe import Recipe, foreign_key

from users.choices import Gender

PatientUser = Recipe(
    get_user_model(),
    username=functools.partial(gen_string, 10),
    email="am.naimi@gmail.com",
    first_name="Amir",
    last_name="Naeimi",
    is_staff=True,
    is_superuser=False,
)

SurgeonUser = Recipe(
    get_user_model(),
    username=functools.partial(gen_string, 10),
    email="am.naimi@gmail.com",
    first_name="Parisa",
    last_name="Rahbari",
    is_staff=True,
    is_superuser=False,
)


Patient = Recipe(
    "users.Patient",
    user=foreign_key(PatientUser),
    gender=Gender.MALE,
    phone_number="+4915901101346",
)

Surgeon = Recipe(
    "users.Surgeon",
    user=foreign_key(SurgeonUser),
    gender=Gender.FEMALE,
    phone_number="+4915901101345",
)
