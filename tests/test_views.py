import datetime
import pytest
from django.core import mail
from django.urls import reverse
from django.utils.timezone import is_aware, now as django_now

from tokenauth.models import AuthToken
from tokenauth.views import awarify
from tests.factories import AuthTokenFactory, UserFactory
from tests.helpers import message_texts


def test_awarify():
    assert is_aware(awarify(datetime.datetime.now())) is True
    assert is_aware(awarify(django_now())) is True


@pytest.mark.django_db
@pytest.mark.parametrize("post_data", [{}, {"email": "hurrr"}])
def test_email_post_invalid_emails(client, post_data):
    response = client.post(reverse("tokenauth:login"), data=post_data)
    assert response.status_code == 302
    assert message_texts(response) == [
        "The email address was invalid. Please check the address and try again."
    ]


@pytest.mark.django_db
def test_email_post_when_already_logged_in(client):
    client.force_login(UserFactory())
    response = client.post(reverse("tokenauth:login"))
    assert response.status_code == 302
    assert message_texts(response) == ["You are already logged in."]


@pytest.mark.django_db
def test_email_post_successful(client):
    user = UserFactory()
    response = client.post(reverse("tokenauth:login"), data={"email": user.email})
    assert response.status_code == 302
    assert message_texts(response) == [
        "Login email sent! Please check your inbox and click on the link to be logged in."
    ]
    assert len(mail.outbox) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("use_next_url", ["/wat/", ""])
def test_token_post_works(client, use_next_url):
    token = AuthTokenFactory(email=UserFactory().email, next_url=use_next_url)
    response = client.get(
        reverse("tokenauth:login-token", kwargs={"token": token.token})
    )
    assert response.status_code == 302
    assert response["Location"] == use_next_url or "/"
    assert message_texts(response) == ["Login successful."]
    assert client.get("/authenticated/").content == b"authenticated"


@pytest.mark.django_db
def test_token_post_already_authenticated(client):
    user = UserFactory()
    token = AuthTokenFactory(email=user.email)
    client.force_login(user)
    response = client.get(
        reverse("tokenauth:login-token", kwargs={"token": token.token})
    )
    assert response.status_code == 302
    assert message_texts(response) == ["You are already logged in."]


@pytest.mark.django_db
def test_token_post_with_junk_token(client):
    response = client.get(reverse("tokenauth:login-token", kwargs={"token": "hurf"}))
    assert response.status_code == 302
    assert message_texts(response) == [
        "The login link is invalid or has expired, or you are not allowed to log in. Please try again."
    ]
    assert client.get("/authenticated/").content == b"unauthenticated"


@pytest.mark.django_db
def test_token_post_with_expired_token(client):
    token = AuthTokenFactory(email=UserFactory().email)
    token.timestamp = django_now() - datetime.timedelta(seconds=3600 * 24 * 365)
    token.save()

    response = client.get(
        reverse("tokenauth:login-token", kwargs={"token": token.token})
    )
    assert response.status_code == 302

    assert message_texts(response) == [
        "The login link is invalid or has expired, or you are not allowed to log in. Please try again."
    ]

    # Check that the expired token has been deleted.
    assert AuthToken.objects.count() == 0

    # Check that we haven't actually logged in.
    assert client.get("/authenticated/").content == b"unauthenticated"


@pytest.mark.django_db
def test_logout(client):
    client.force_login(UserFactory())
    assert client.get("/authenticated/").content == b"authenticated"
    response = client.get(reverse("tokenauth:logout"))
    assert message_texts(response) == ["You have been logged out."]
    assert client.get("/authenticated/").content == b"unauthenticated"
