from model_bakery.recipe import Recipe

HealthProvider = Recipe(
    "health_providers.HealthProvider",
    name="Atieh",
    phone_number="+4915901101346",
    email="atieh@gmail.com",
    is_hospital=True,
)
