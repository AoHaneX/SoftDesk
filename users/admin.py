from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        (
            "Informations supplémentaires",
            {
                "fields": (
                    "age",
                    "can_be_contacted",
                    "can_data_be_shared",
                    "created_time",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Informations supplémentaires",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "age",
                    "can_be_contacted",
                    "can_data_be_shared",
                )
            },
        ),
    )

    readonly_fields = ("created_time",)