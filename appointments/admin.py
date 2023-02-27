from django.contrib import admin

from appointments.models import Appointment, SurgeonAvailabilitySlot


class AppointmentInline(admin.TabularInline):
    extra = 2
    model = Appointment

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.select_related(
            "appointment_slot",
            "patient",
        )

    def has_change_permission(self, request, obj=None):
        return False


class SurgeonAvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ("surgeon", "health_provider", "start_datetime")
    search_fields = ("surgeon", "health_provider")
    inlines = [AppointmentInline]

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.select_related(
            "surgeon",
            "health_provider",
            "surgeon__user",
        )


admin.site.register(SurgeonAvailabilitySlot, SurgeonAvailabilitySlotAdmin)
