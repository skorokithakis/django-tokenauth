import datetime
import pytest
from django.core import mail
from django.urls import reverse
from django.utils.timezone import is_aware, now as django_now

from tokenauth.views import awarify
from tests.factories import UserFactory
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
