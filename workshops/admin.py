from django.contrib import admin
from .models import Registration, Workshop


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "capacity")
    readonly_fields = ("admin_token",)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "workshop", "status", "created_at")
    list_filter = ("workshop", "status")