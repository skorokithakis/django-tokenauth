import factory
from django.contrib.auth import get_user_model

from tokenauth.models import AuthToken


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda i: f"user{i}")
    email = factory.Sequence(lambda i: f"imaginary{i}@example.invalid")
    password = factory.django.Password("password")


class AuthTokenFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda i: f"imaginary{i}@example.invalid")

    class Meta:
        model = AuthToken
