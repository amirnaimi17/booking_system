from django.contrib import admin

from users.models import Patient, Surgeon


class SurgeonAdmin(admin.ModelAdmin):
    list_display = (
        "user_username",
        "user_email",
    )
    search_fields = ("user_email", "user_first_name", "user_last_name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.select_related(
            "user",
        )

    def user_email(self, obj):
        return obj.user.email

    def user_username(self, obj):
        return obj.user.username

    def user_first_name(self, obj):
        return obj.user.first_name

    def user_last_name(self, obj):
        return obj.user.last_name

    user_email.short_description = "Email"
    user_first_name.short_description = "First Name"
    user_last_name.short_description = "Last Name"
    user_username.short_description = "Username"


admin.site.register(Surgeon, SurgeonAdmin)


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "user_username",
        "user_email",
    )
    search_fields = ("user_email", "user_first_name", "user_last_name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.select_related(
            "user",
        )

    def user_email(self, obj):
        return obj.user.email

    def user_username(self, obj):
        return obj.user.username

    def user_first_name(self, obj):
        return obj.user.first_name

    def user_last_name(self, obj):
        return obj.user.last_name

    user_email.short_description = "Email"
    user_first_name.short_description = "First Name"
    user_last_name.short_description = "Last Name"
    user_username.short_description = "Username"


admin.site.register(Patient, PatientAdmin)
