from django.contrib.auth import get_user_model

from .models import AuthToken, generate_token


class EmailTokenBackend:
    def get_user(self, user_id):
        """Get a user by their primary key."""
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, token=None):
        """Authenticate a user given a signed token."""
        AuthToken.delete_stale()

        t = AuthToken.objects.filter(token=token).first()
        if not t:
            return
        else:
            t.delete()

        User = get_user_model()

        if "username" in [field.name for field in User._meta.get_fields(include_hidden=True)]:
            # The model contains a username, so we should try to fill it in.
            user, created = User.objects.get_or_create(email=t.email, defaults={"username": "u" + generate_token()[:8]})
        else:
            user, created = User.objects.get_or_create(email=t.email)

        if t.next_url:
            # This is a bit of a hack so we can return the URL to redirect to.
            user._tokenauth_next_url = t.next_url
        return user
