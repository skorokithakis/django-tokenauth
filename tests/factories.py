import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda i: f"user{i}")
    email = factory.Sequence(lambda i: f"imaginary{i}@example.invalid")
    password = factory.django.Password("password")
