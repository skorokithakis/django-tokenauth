from datetime import timedelta

import pytest
from django.utils.timezone import now

from tests.factories import AuthTokenFactory
from tokenauth.models import AuthToken, EmailLog, generate_token


def test_emaillog_str():
    assert str(EmailLog(email="example@example.invalid")) == "example@example.invalid"


def test_generate_token():
    # No really interesting tests we can do here; just make sure it's
    # returning something.
    token = generate_token()
    assert isinstance(token, str)
    assert len(token) == 8

    # ...and that we haven't done something terminally bad.
    assert generate_token() != token


@pytest.mark.django_db
def test_authtoken_delete_stale():
    expired_token = AuthTokenFactory()
    # creating with `timestamp` kwarg doesn't actually work (probably because
    # of auto_now_add)
    expired_token.timestamp = now() - timedelta(days=1)
    expired_token.save()
    alive_token = AuthTokenFactory()

    AuthToken.delete_stale()
    assert AuthToken.objects.count() == 1
    assert AuthToken.objects.get() == alive_token
