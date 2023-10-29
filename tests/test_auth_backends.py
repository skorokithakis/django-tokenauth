import sys

import pytest

from tokenauth.auth_backends import EmailTokenBackend
from tests.factories import UserFactory


@pytest.mark.django_db
def test_emailtoken_backend_get_user():
    user = UserFactory()
    backend = EmailTokenBackend()
    assert backend.get_user(user.pk) == user
    assert backend.get_user(None) is None
    assert backend.get_user(sys.maxsize) is None
