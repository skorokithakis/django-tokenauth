from django import forms
from django.contrib import messages
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from . import settings as ta_settings
from .helpers import email_login_link


class EmailForm(forms.Form):
    """The email form for the login page."""

    email = forms.EmailField(label="Your email address")


def token_post(request):
    if request.user.is_authenticated:
        messages.error(request, _("You are already logged in."))
        return redirect(ta_settings.LOGIN_REDIRECT)

    if request.GET.get("d"):
        # The user has clicked a login link.
        user = authenticate(token=request.GET["d"])
        if user is None:
            messages.error(request, _("The login link was invalid or has expired. Please try to log in again."))
            return redirect(ta_settings.LOGIN_URL)

        djlogin(request, user)
        messages.success(request, _("Login successful."))
        return redirect(ta_settings.LOGIN_REDIRECT)
    elif request.method == "POST":
        # The user has submitted the email form.
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

        email_login_link(request, email)

        messages.success(
            request, _("Login email sent! Please check your inbox and click on the link to be logged in.")
        )
    else:
        messages.error(request, _("The login link was invalid. Please try to log in again."))

    return redirect(ta_settings.LOGIN_URL)


@login_required
def logout(request):
    djlogout(request)
    messages.success(request, _("You have been logged out."))
    return redirect(ta_settings.LOGOUT_REDIRECT)
