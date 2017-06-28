import base64
import json
import time

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login as djlogin, logout as djlogout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.signing import Signer
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from . import settings as ta_settings


class EmailForm(forms.Form):
    """The email form for the login page."""

    email = forms.EmailField(label="Your email address")


def token_post(request):
    if request.user.is_authenticated():
        messages.error(request, _("You are already logged in."))
        return redirect(ta_settings.LOGIN_REDIRECT)

    if request.GET.get("d"):
        # The user has clicked a login link.
        user = authenticate(token=request.GET["d"])
        if user is not None:
            djlogin(request, user)
            messages.success(request, _("Login successful."))
            return redirect(ta_settings.LOGIN_REDIRECT)
        else:
            messages.error(request, _("The login link was invalid or has expired. Please try to log in again."))
    elif request.method == "POST":
        # The user has submitted the email form.
        form = EmailForm(request.POST)
        if form.is_valid():
            current_site = get_current_site(request)

            # Create the signed structure containing the time and email address.
            email = form.cleaned_data["email"].lower().strip()
            data = {"t": int(time.time()), "e": email}
            data = Signer().sign(base64.b64encode(json.dumps(data).encode("utf8")))

            # Send the link by email.
            send_mail(
                render_to_string("tokenauth_login_subject.txt", {"current_site": current_site}, request=request).strip(),
                render_to_string("tokenauth_login_body.txt", {"current_site": current_site, "data": data}, request=request),
                ta_settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, _("Login email sent! Please check your"
                " inbox and click on the link to be logged in."))
        else:
            messages.error(request, _("The email address was invalid. Please"
                " check the address and try again."))
    else:
        messages.error(request, _("The login link was invalid or has expired. Please try to log in again."))

    return redirect(ta_settings.LOGIN_URL)


@login_required
def logout(request):
    djlogout(request)
    messages.success(request, _("You have been logged out."))
    return redirect(ta_settings.LOGOUT_REDIRECT)
