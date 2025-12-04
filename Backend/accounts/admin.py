from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("username", "email", "nombre", "apellido", "rol", "is_staff", "is_active")
    list_filter = ("rol", "is_staff", "is_active")

    fieldsets = UserAdmin.fieldsets + (
        ("Información adicional", {
            "fields": ("nombre", "apellido", "rol"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Información adicional", {
            "fields": ("nombre", "apellido", "rol"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
