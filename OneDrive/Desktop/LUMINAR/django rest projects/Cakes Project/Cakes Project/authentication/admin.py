from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


@admin.register(models.profile)
class ProfileAdmin(UserAdmin):
    list_display = (*UserAdmin.list_display, "role")
    fieldsets = UserAdmin.fieldsets + (
        ("Profile", {"fields": ("role",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Profile", {"fields": ("role",)}),
    )