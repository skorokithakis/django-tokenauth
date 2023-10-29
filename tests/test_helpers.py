from urllib.parse import urlparse

import pytest
from django.core import mail
from django.test import RequestFactory

from tests.factories import UserFactory
from tests.helpers import message_texts
from tokenauth.helpers import email_login_link
from tokenauth.models import AuthToken


@pytest.mark.django_db
def test_email_login_link(client):
    # paranoia about test pollution
    assert AuthToken.objects.count() == 0

    email_login_link(
        RequestFactory().get("/"), "imaginary@example.invalid", next_url="/wat/"
    )
    assert len(mail.outbox) == 1
    sent_mail = mail.outbox[0]
    assert sent_mail.to == ["imaginary@example.invalid"]
    assert sent_mail.subject == "Your login link"
    assert sent_mail.body.startswith("Hello!")

    token = AuthToken.objects.get()
    assert token.next_url == "/wat/"
    assert token.email == "imaginary@example.invalid"
    assert token.token

    # Make sure the link in the email does what we think it does.
    url = next(
        line for line in sent_mail.body.split("\n") if line.startswith("https://")
    )
    path = urlparse(url).path

    response = client.get(path)
    assert response.status_code == 302
    assert response["Location"] == "/wat/"
    assert message_texts(response) == ["Login successful."]
    # Make sure we've actually logged in.
    assert client.get("/authenticated/").content == b"authenticated"


@pytest.mark.django_db
def test_email_login_link_with_new_email(client):
    user = UserFactory(email="imaginary@example.invalid")

    # paranoia about test pollution again
    assert AuthToken.objects.count() == 0

    email_login_link(
        RequestFactory().get("/"),
        "imaginary@example.invalid",
        new_email="imaginary2@example.invalid",
    )
    assert len(mail.outbox) == 1
    sent_mail = mail.outbox[0]
    assert sent_mail.to == ["imaginary2@example.invalid"]
    assert sent_mail.subject == "Please confirm your email address change"
    assert sent_mail.body.startswith("Hello!")

    token = AuthToken.objects.get()
    assert token.email == "imaginary@example.invalid"
    assert token.token

    # Make sure the link in the email does what we think it does.
    url = next(
        line for line in sent_mail.body.split("\n") if line.startswith("https://")
    )
    path = urlparse(url).path

    response = client.get(path)
    assert response.status_code == 302
    assert response["Location"] == "/accounts/profile/"
    assert message_texts(response) == ["Your email address has been changed."]

    # Has the email address changed?
    user.refresh_from_db()
    assert user.email == "imaginary2@example.invalid"
