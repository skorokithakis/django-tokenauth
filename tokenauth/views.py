from datetime import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.timezone import is_aware
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from . import settings as ta_settings
from .helpers import email_login_link
from .models import EmailLog

try:
    # Try importing django-ratelimit.
    from ratelimit.decorators import ratelimit as rl

    ratelimit = rl(key="ip", rate=ta_settings.RATELIMIT_RATE)
except ImportError:
    try:
        # Try importing django-brake.
        from brake.decorators import ratelimit as rl

        ratelimit = rl(rate=ta_settings.RATELIMIT_RATE)
    except ImportError:
        # Neither exists, so no rate-limiting.
        def ratelimit(func):
            return func


class EmailForm(forms.Form):
    """The email form for the login page."""

    email = forms.EmailField(label="Your email address")


def awarify(dt):
    """Make a datetime aware if it's not already."""
    if is_aware(dt):
        return dt
    else:
        return make_aware(dt)


@require_http_methods(["POST"])
@ratelimit
def email_post(request):
    """Process the submission of the form with the user's email and mail them a link."""
    if getattr(request, "limited", False):
        messages.warning(
            request, _("You're trying to log in too often. Please try again later.")
        )
        return redirect(ta_settings.LOGIN_URL)

    if request.user.is_authenticated:
        messages.error(request, _("You are already logged in."))
        return redirect(ta_settings.LOGIN_REDIRECT)

    form = EmailForm(request.POST)
    if not form.is_valid():
        messages.error(
            request,
            _("The email address was invalid. Please check the address and try again."),
        )
        return redirect(ta_settings.LOGIN_URL)

    email = ta_settings.NORMALIZE_EMAIL(form.cleaned_data["email"])
    if not email:
        # The user's normalization function has returned something falsy.
        messages.error(
            request,
            _(
                "That email address is not allowed to authenticate. Please use an alternate address."
            ),
        )
        return redirect(ta_settings.LOGIN_URL)

    EmailLog.delete_stale()
    previous_emails = EmailLog.objects.filter(email=email)
    if previous_emails:
        # The user already requested an email a short time ago.
        messages.error(
            request,
            _(
                "You have already requested an email. Please wait %(delay)s more seconds before requesting another."
            )
            % {
                "delay": ta_settings.RESENDING_DELAY
                - (
                    awarify(datetime.now()) - awarify(previous_emails[0].timestamp)
                ).seconds
            },
        )
        return redirect(ta_settings.LOGIN_URL)

    email_login_link(request, email, next_url=request.GET.get("next", ""))

    messages.success(
        request,
        _(
            "Login email sent! Please check your inbox and click on the link to be logged in."
        ),
    )
    return redirect(ta_settings.LOGIN_URL)


@require_http_methods(["GET"])
def token_post(request, token):
    """Validate the token the user submitted."""
    user = authenticate(request, token=token)
    if user is None:
        messages.error(
            request,
            _(
                "The login link is invalid or has expired, or you are not allowed to "
                "log in. Please try again."
            ),
        )
        return redirect(ta_settings.LOGIN_URL)

    if hasattr(user, "_tokenauth_new_email"):
        user.email = user._tokenauth_new_email
        try:
            user.save()
        except Exception:
            messages.error(
                request, _("There was an error changing your email address.")
            )
        else:
            messages.success(request, _("Your email address has been changed."))

        del user._tokenauth_new_email
        return redirect(ta_settings.LOGIN_REDIRECT)

    if request.user.is_authenticated:
        messages.error(request, _("You are already logged in."))
        return redirect(ta_settings.LOGIN_REDIRECT)

    if hasattr(user, "_tokenauth_next_url"):
        # Get the next URL from the user object, if it was set by our custom `authenticate`.
        next_url = user._tokenauth_next_url

        # Remove the next URL from the user object.
        del user._tokenauth_next_url
    else:
        next_url = ta_settings.LOGIN_REDIRECT

    djlogin(request, user)
    messages.success(request, _("Login successful."))
    return redirect(next_url)


@login_required
def logout(request):
    djlogout(request)
    messages.success(request, _("You have been logged out."))
    return redirect(ta_settings.LOGOUT_REDIRECT)
