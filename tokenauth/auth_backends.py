from django.contrib.auth import get_user_model

from .models import AuthToken


class EmailTokenBackend:
    def get_user(self, user_id):
        """Get a user by their primary key."""
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, token=None):
        """Authenticate a user given a signed token."""
        AuthToken.delete_stale()

        t = AuthToken.objects.filter(token=token).first()
        if not t:
            return
        else:
            t.delete()

        User = get_user_model()

        user, created = User.objects.get_or_create(email=t.email)
        if t.next_url:
            # This is a bit of a hack so we can return the URL to redirect to.
            user._tokenauth_next_url = t.next_url
        return user
