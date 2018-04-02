from django.contrib import admin

from .models import AuthToken


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ["email", "timestamp", "next_url"]
    ordering = ["-timestamp"]
