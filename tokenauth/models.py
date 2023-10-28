import secrets
from datetime import timedelta

from django.db import models
from django.utils.timezone import now

from . import settings as ta_settings


def generate_token():
    return "".join(
        [
            secrets.choice("abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789")
            for _ in range(ta_settings.TOKEN_LENGTH)
        ]
    )


class EmailLog(models.Model):
    """
    A log of the last time an email was sent, for rate-limiting.

    Rate-limiting based on IP addresses is great to prevent abuse, but some
    users keep impatiently sending themselves emails, causing grey- or
    blacklisting. This class keeps track of when each email was sent, to
    allow you to throttle the frequency.
    """

    email = models.CharField(max_length=2000, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    @classmethod
    def delete_stale(cls):
        """
        Delete stale log entries, ie entries that are more than
        RESENDING_DELAY seconds old.
        """
        cls.objects.filter(
            timestamp__lt=now() - timedelta(seconds=ta_settings.RESENDING_DELAY)
        ).delete()

    def __str__(self):
        return self.email


class AuthToken(models.Model):
    token = models.CharField(max_length=200, default=generate_token, primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    email = models.CharField(max_length=2000)
    new_email = models.CharField(
        max_length=2000,
        help_text="The email address that the user's email will be set to when they use this token.",
        blank=True,
    )
    next_url = models.CharField(max_length=2000, blank=True)

    @classmethod
    def delete_stale(cls):
        """
        Delete stale tokens, ie tokens that are more than
        TOKEN_DURATION seconds old.
        """
        cls.objects.filter(
            timestamp__lt=now() - timedelta(seconds=ta_settings.TOKEN_DURATION)
        ).delete()

    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
