Changelog
=========


%%version%% (unreleased)
------------------------

Fixes
~~~~~
- Return early on error. [Stavros Korokithakis]


v0.5.4 (2025-08-02)
-------------------

Fixes
~~~~~
- Support Django 4.2, and add a pile of tests (#5) [Lewis Collard]

  * Only bother testing modern Django and Python versions.

  Django 3.2 is out of support in a few months. Anyone adding this to a new
  project will be using 4.2 if they have any sense. If they have no sense,
  they can probably continue with the old version.

  * Add initial skeleton for tests.

  * Use `secrets.choice` rather than `random.choice` for generating tokens.

  random.choice is not cryptographically secure. It might be impossible to
  exploit with network timings. It is also not worth risking.

  * Use modern `django.urls.path` for URLs.

  * Use gettext_lazy, not the now-disappeared ugettext_lazy.

  * Add some tests for views.

  * Add tests for admin.

  * Add tests for email_login_link.

  * Add .venv to gitignore.

  * Add test for AuthToken.delete_stale.

  * Make help_text for TokenAuth.new_email translatable.

  While I'm there, I wasn't sure if this was going to add a migration changing
  from str to a lazy object, so add a test to ensure that no new migrations
  are needed.

  * Add Black formatting check to tests.

  * Add tests for `awarify`.

  * Add tests for EmailTokenBackend.get_user.

  * Now that we have tests for the behaviour, simplify EmailTokenBackend.get_user.

  .first() will return None if no such user exists, and we should very well
  hope that we will never have two users with the same primary key, so
  `.filter(pk=xx).first()` does the same thing as try/except.

  * Add a bunch of tests for the login/logout views.

  * Add required Django version to README.md.

  * Restore testing of 3.x and 2.x.

  * Exclude `tests` from `find_namespace_packages`.

  * Remove an unused import.

  * Run `pre-commit` instead of `black` directly.


v0.5.3 (2023-05-21)
-------------------

Features
~~~~~~~~
- Include detail about ignoring this message. [Stavros Korokithakis]


v0.5.2 (2021-11-13)
-------------------

Fixes
~~~~~
- Don't crash on an email-change error. [Stavros Korokithakis]


v0.5.1 (2021-06-26)
-------------------

Fixes
~~~~~
- Fix naive/aware datetime issue. [Stavros Korokithakis]


v0.5.0 (2021-06-12)
-------------------

Features
~~~~~~~~
- Add delay between two subsequent emails. [Stavros Korokithakis]
- Add CAN_LOG_IN setting to disallow logins to specific users. [Stavros
  Korokithakis]

Fixes
~~~~~
- Add wording about the link being temporary. [Stavros Korokithakis]
- Normalize email addresses in the email change form. [Stavros
  Korokithakis]


v0.2.4 (2019-10-27)
-------------------

Fixes
~~~~~
- Pass request to authenticate method (#2) [Theodore Keloglou]


v0.2.3 (2018-07-09)
-------------------

Fixes
~~~~~
- Add better check for the existence of a username field. [Stavros
  Korokithakis]


v0.2.2 (2018-06-10)
-------------------

Fixes
~~~~~
- Don't create new users every login. [Stavros Korokithakis]


v0.2.1 (2018-06-10)
-------------------

Fixes
~~~~~
- If the User model has a username field, try to fill it in. [Stavros
  Korokithakis]


v0.2.0 (2018-04-02)
-------------------

Features
~~~~~~~~
- Add ?next= parameter. [Stavros Korokithakis]
- Make tokens dramatically shorter by using the database to store them.
  [Stavros Korokithakis]


v0.1.0 (2018-02-09)
-------------------

Features
~~~~~~~~
- Allow normalizing/authorizing email addresses with the NORMALIZE_EMAIL
  setting. [Stavros Korokithakis]


v0.0.6 (2018-02-07)
-------------------

Features
~~~~~~~~
- Add helper function to email the user's login link to them. [Stavros
  Korokithakis]

Fixes
~~~~~
- Add app_name for Django 2.0. [Stavros Korokithakis]
- Django 2 compatibility. [Stavros Korokithakis]

  Merge pull request #1 from sirodoht/django-2
- Tokenauth template should be given a string, not a bytestring.
  [Theodore Keloglou]

  As of Django 2.0 Signer.sign returns a bytestring if given one.
  We want to pass a utf8 string to our template, thus we need to
  decode it after base64-encoding it.
- Is_authenticated is now only an attribute. [Theodore Keloglou]

  As of Django 1.10 is_authenticated became an attribute rather
  than a function and the deprecation period lasted until Django 2.0,
  which left is_authenticated only as a boolean variable.

Documentation
~~~~~~~~~~~~~
- Add settings section to the documentation. [Stavros Korokithakis]


v0.0.4 (2017-06-28)
-------------------

Fixes
~~~~~
- Include template files. [Stavros Korokithakis]


v0.0.3 (2017-06-28)
-------------------

Fixes
~~~~~
- Use the LOGIN_REDIRECT_URL if the LOGOUT_REDIRECT_URL is not
  specified. [Stavros Korokithakis]


