import pytest
from model_bakery import baker
from rest_framework.authtoken.models import Token


@pytest.fixture
def patient(db):
    return baker.make_recipe(
        "users.Patient",
    )


@pytest.fixture
def surgeon(db):
    return baker.make_recipe(
        "users.Surgeon",
    )


@pytest.fixture
def user_patient(db):
    return baker.make_recipe(
        "users.Patient",
    )


# @pytest.fixture
# def surgeon(db):
#     return baker.make_recipe(
#         "users.Surgeon",
#     )


@pytest.fixture
def health_provider(db):
    return baker.make_recipe(
        "health_providers.HealthProvider",
    )


@pytest.fixture
def token(db, patient):
    return Token.objects.create(user=patient.user)
