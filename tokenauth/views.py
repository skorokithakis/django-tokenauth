from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods

from . import settings as ta_settings
from .helpers import email_login_link


class EmailForm(forms.Form):
    """The email form for the login page."""

    email = forms.EmailField(label="Your email address")


@require_http_methods(["POST"])
def email_post(request):
    """Process the submission of the form with the user's email and mail them a link."""
    if request.user.is_authenticated:
        messages.error(request, _("You are already logged in."))
        return redirect(ta_settings.LOGIN_REDIRECT)

    form = EmailForm(request.POST)
    if not form.is_valid():
        messages.error(request, _("The email address was invalid. Please check the address and try again."))
        return redirect(ta_settings.LOGIN_URL)

    email = ta_settings.NORMALIZE_EMAIL(form.cleaned_data["email"])
    if not email:
        # The user's normalization function has returned something falsy.
        messages.error(
            request, _("That email address is not allowed to authenticate. Please use an alternate address.")
        )
        return redirect(ta_settings.LOGIN_URL)

    email_login_link(request, email, next_url=request.GET.get("next", ""))

    messages.success(request, _("Login email sent! Please check your inbox and click on the link to be logged in."))
    return redirect(ta_settings.LOGIN_URL)


@require_http_methods(["GET"])
def token_post(request, token):
    """Validate the token the user submitted."""
    if request.user.is_authenticated:
        messages.error(request, _("You are already logged in."))
        return redirect(ta_settings.LOGIN_REDIRECT)

    user = authenticate(request, token=token)
    if user is None:
        messages.error(request, _("The login link was invalid or has expired. Please try to log in again."))
        return redirect(ta_settings.LOGIN_URL)

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
