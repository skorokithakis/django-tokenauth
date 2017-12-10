import base64
import json
import time

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.signing import Signer
from django.template.loader import render_to_string

from . import settings as ta_settings


def email_login_link(request, email):
    current_site = get_current_site(request)

    # Create the signed structure containing the time and email address.
    email = email.lower().strip()
    data = {"t": int(time.time()), "e": email}
    data = json.dumps(data).encode("utf8")
    data = Signer().sign(base64.b64encode(data).decode("utf8"))

    # Send the link by email.
    send_mail(
        render_to_string("tokenauth_login_subject.txt", {"current_site": current_site}, request=request).strip(),
        render_to_string("tokenauth_login_body.txt", {"current_site": current_site, "data": data}, request=request),
        ta_settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
