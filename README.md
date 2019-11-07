django-tokenauth
================

About
-----

Django-tokenauth is a simple, passwordless authentication method based on
a one-time token sent over email. There is no user registration per se, only
login. The user enters their email on the login page, and a one-time link that
is only valid for a few minutes (and one login) is generated and sent in an
email. The user clicks on the link and is immediately logged in, and the token
is invalidated.

[![PyPI version](https://img.shields.io/pypi/v/django-tokenauth.svg)](https://pypi.python.org/pypi/django-tokenauth)


Installing django-tokenauth
---------------------------

* Install django-tokenauth using pip: `pip install django-tokenauth`

* Add `tokenauth` to your `INSTALLED_APPS`:

```python
# settings.py
INSTALLED_APPS = [... 'tokenauth', ...]
```

* Add tokenauth to your authentication backends:

```python
AUTHENTICATION_BACKENDS = (
    'tokenauth.auth_backends.EmailTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
)
```

* Add the tokenauth URL to your `urls.py`:

```python
# urls.py
urlpatterns += url(r'^auth/', include('tokenauth.urls', namespace="tokenauth"))
```

* Add a form to the page where you want to authenticate a user:

```html
<form action="{% url "tokenauth:login" %}?next={{ request.GET.next }}" method="post">{% csrf_token %}
    <input name="email" type="email" autofocus />
    <button type="submit">Submit</button>
</form>
```

Done! The user enters their email, click the link and they're in. No passwords
or anything.

You can email a user a login link by using the
`tokenauth.helpers.email_login_link` convenience function:

```python
from tokenauth.helpers import email_login_link

def myview(request):
    ...
    email_login_link(request, "some@email.address", next_url="/some/page/")
    ...
```

`email_login_link` accepts an optional `next_url` parameter, which, if set,
will tell `tokenauth` to redirect that user to that URL after a successful
login. If this is not specified, the user will be redirected to the URL that
is specified in the `TOKENAUTH_LOGIN_REDIRECT` setting.

To log someone out, just redirect them to `tokenauth:logout` (or use Django's
built-in function, or roll your own. It's just standard logout).


Rate-limiting
-------------

django-tokenauth supports ratelimiting for the email-sending view (so you don't
spam people). To enable it, just install `django-ratelimit` or `django-brake`.
The library will automatically start rate-limiting requests (see "settings"
below for the rate).

**Warning:** Since these libraries use IPs for rate-limiting, you need to make
sure your application gets the correct user IP. Specifically, if you use a
reverse proxy, the application might be getting the proxy's IP instead, and
blocking everyone. Ensure your application can see the real user's IP before
enabling rate-limiting.

Also, make sure your cache works properly, since `ratelimit` and `brake` use it
to remember requests.


Settings
--------

Here are the settings you can change in your `settings.py`:

* `TOKENAUTH_NORMALIZE_EMAIL` (default: `lambda e: e`): A function that will accept a single argument, the email address
  the user specifies in the form, and will normalize it.  You may want to use this for lowercasing email addresses, or
  for removing spaces from the beginning and end. You can also use this for disallowing authentication, as an email
  address will not be allowed to authenticate if this function returns something falsy (False, or None, or the empty
  string).
* `TOKENAUTH_TOKEN_DURATION` (default: 30 minutes): How long a token should be valid for, in seconds.
* `TOKENAUTH_TOKEN_LENGTH` (default: 8): How many characters long the token should be. The longer the validity, the
  longer the length, to maintain security. The longer the length, the worse the UX if a user has to type it in manually.
* `TOKENAUTH_LOGIN_URL` (default: LOGIN_URL): Where to redirect after the email link has been clicked.
* `TOKENAUTH_LOGIN_REDIRECT` (default: LOGIN_REDIRECT_URL): Where to redirect after login.
* `TOKENAUTH_LOGOUT_REDIRECT` (default: LOGOUT_REDIRECT_URL): Where to redirect after logout.
* `TOKENAUTH_DEFAULT_FROM_EMAIL` (default: DEFAULT_FROM_EMAIL): The email address the activation email should come from.
* `TOKENAUTH_RATELIMIT_RATE` (default: "3/h"): How many requests per IP to allow for email sending.


FAQ
---

### But but... isn't this insecure? What if the user's email gets compromised?

Do you have a "forgot your password?" link? That does exactly the same thing, so this library is more secure than that,
since it ensures nobody can steal a user's password (since there is none).

### Is this library amazing?

Yes, yes it is. It even redirects the user to the page they were trying to go before the login page. Not only that, but
the signin link is really short, so they can even log in securely on an untrusted computer by receiving the email on
their phone and typing it on the untrusted computer.


License
-------

This software is distributed under the BSD license.
