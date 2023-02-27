from django.contrib import admin

from health_providers.models import HealthProvider


class HealthProviderAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_clinic",
        "is_hospital",
        "email",
    )
    list_filter = (
        "name",
        "is_clinic",
        "is_hospital",
    )
    search_fields = ("name", "is_clinic", "is_hospital")


admin.site.register(HealthProvider, HealthProviderAdmin)
