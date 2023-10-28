import getpass
import os

import pytest
from django.conf import settings


def pytest_configure():
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": os.environ.get(
                    "TOKENAUTH_DB_BACKEND", "django.db.backends.postgresql"
                ),
                "NAME": os.environ.get("TOKENAUTH_DB_NAME", "tokenauth_test"),
                "USER": os.environ.get("TOKENAUTH_DB_USER", getpass.getuser()),
                "PASSWORD": os.environ.get("TOKENAUTH_DB_PASSWORD"),
            }
        },
        TIME_ZONE="UTC",
        INSTALLED_APPS=[
            # Django apps
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.messages",
            "django.contrib.sessions",
            "tokenauth",
        ],
        ROOT_URLCONF="tests.urls",
        ALLOWED_HOSTS=["*"],
        LANGUAGE_CODE="en",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.contrib.auth.context_processors.auth",
                        "django.template.context_processors.i18n",
                        "django.contrib.messages.context_processors.messages",
                        "django.template.context_processors.request",
                    ]
                },
            }
        ],
        AUTHENTICATION_BACKENDS=[
            "tokenauth.auth_backends.EmailTokenBackend",
            "django.contrib.auth.backends.ModelBackend",
        ],
        MIDDLEWARE=[
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
        ],
        SECRET_KEY="KNOWN_FIXED_VALUE_IS_FINE_FOR_TESTS",
    )
