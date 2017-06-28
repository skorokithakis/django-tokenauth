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


License
-------

This software is distributed under the BSD license.
