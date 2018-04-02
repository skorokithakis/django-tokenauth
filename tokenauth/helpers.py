from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string

from . import settings as ta_settings
from .models import AuthToken


def email_login_link(request, email, next_url=""):
    current_site = get_current_site(request)

    # Create the token.
    email = email.lower().strip()
    token = AuthToken.objects.create(email=email, next_url=next_url)

    # Send the link by email.
    send_mail(
        render_to_string("tokenauth_login_subject.txt", {"current_site": current_site}, request=request).strip(),
        render_to_string("tokenauth_login_body.txt", {"current_site": current_site, "token": token}, request=request),
        ta_settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
