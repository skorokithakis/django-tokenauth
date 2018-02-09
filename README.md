django-tokenauth
================

About
-----

Django-tokenauth is a simple, passwordless authentication method based on
a one-time token sent over email. There is no user registration per se, only
login. The user enters their email on the login page, and a one-time link that
is only valid for a few minutes  is generated and sent in an email. The user
clicks on the link and is immediately logged in.

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
<form action="{% url "tokenauth:login" %}" method="post">{% csrf_token %}
    <input name="email" type="email" />
    <button type="submit">Submit</button>
</form>
```

Done! The user enters their email, click the link and they're in. No passwords
or anything.

You can email a user a login link by using the
`tokenauth.helpers.email_login_link` convenience function;

```python
from tokenauth.helpers import email_login_link

def myview(request):
    ...
    email_login_link(request, "some@email.address")
    ...
```


Settings
--------

Here are the settings you can change in your `settings.py`:

* `TOKENAUTH_NORMALIZE_EMAIL` (default: `lambda e: e`): A function that will accept a single argument, the email address
  the user specifies in the form, and will normalize it.  You may want to use this for lowercasing email addresses, or
  for removing spaces from the beginning and end. You can also use this for disallowing authentication, as an email
  address will not be allowed to authenticate if this function returns something falsy (False, or None, or the empty
  string).
* `TOKENAUTH_TOKEN_DURATION` (default: 30 minutes): How long a token should be valid for, in seconds.
* `TOKENAUTH_LOGIN_URL` (default: LOGIN_URL): Where to redirect after the email link has been clicked.
* `TOKENAUTH_LOGIN_REDIRECT` (default: LOGIN_REDIRECT_URL): Where to redirect after login.
* `TOKENAUTH_LOGOUT_REDIRECT` (default: LOGOUT_REDIRECT_URL): Where to redirect after logout.
* `TOKENAUTH_DEFAULT_FROM_EMAIL` (default: DEFAULT_FROM_EMAIL): The email address the activation email should come from.


License
-------

This software is distributed under the BSD license.
