import random
from datetime import timedelta

from django.db import models
from django.utils.timezone import now

from . import settings as ta_settings


def generate_token():
    return "".join([random.choice("abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(ta_settings.TOKEN_LENGTH)])


class AuthToken(models.Model):
    token = models.CharField(max_length=200, default=generate_token, primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    email = models.CharField(max_length=2000)
    next_url = models.CharField(max_length=2000, blank=True)

    @classmethod
    def delete_stale(cls):
        """Delete stale tokens, ie tokens that are more than TOKEN_DURATION seconds older."""
        cls.objects.filter(timestamp__lt=now() - timedelta(seconds=ta_settings.TOKEN_DURATION)).delete()

    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
