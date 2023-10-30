import pytest
from django.urls import reverse

from tests.factories import AuthTokenFactory
from tests.factories import UserFactory
from tokenauth.models import AuthToken


@pytest.mark.django_db
def test_auth_token_admin_works(client):
    """
    This is somewhat covered by Django being Django. Nevertheless, let's
    ensure that we have not done something to break the admin in future.
    """
    tokens = AuthTokenFactory.create_batch(10)
    client.force_login(UserFactory(is_staff=True, is_superuser=True))
    response = client.get(reverse("admin:tokenauth_authtoken_changelist"))
    assert response.status_code == 200

    response = client.get(
        reverse("admin:tokenauth_authtoken_change", args=[tokens[0].pk])
    )
    assert response.status_code == 200

    response = client.get(
        reverse("admin:tokenauth_authtoken_change", args=[tokens[0].pk])
    )
    assert response.status_code == 200

    response = client.get(reverse("admin:tokenauth_authtoken_add"))
    assert response.status_code == 200

    response = client.post(
        reverse("admin:tokenauth_authtoken_add"),
        data={
            "email": "createit@example.invalid",
            "token": "abcdef",
        },
    )
    assert response.status_code == 302
    assert AuthToken.objects.count() == 11
