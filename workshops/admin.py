from django.contrib import admin
from .models import Workshop, Registration


admin.site.register(Workshop)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "workshop", "status", "created_at")
    list_filter = ("workshop", "status")