Changelog
=========


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


