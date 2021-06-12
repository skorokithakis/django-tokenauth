from django.contrib import admin

from .models import AuthToken
from .models import EmailLog


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ["email", "timestamp"]
    ordering = ["-timestamp"]


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ["email", "timestamp", "next_url"]
    ordering = ["-timestamp"]
