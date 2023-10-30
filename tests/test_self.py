import pytest

from tests.factories import UserFactory


@pytest.mark.django_db
def test_authenticated_view_works(client):
    # Self-test for our testing "authenticated" view. We depend on it in tests
    # so it is a good idea to make sure it works.
    response = client.get("/authenticated/")
    assert response.status_code == 200
    assert response.content == b"unauthenticated"

    client.force_login(UserFactory())
    response = client.get("/authenticated/")
    assert response.content == b"authenticated"
    assert response.status_code == 200
