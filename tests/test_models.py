from tokenauth.models import EmailLog, generate_token


def test_emaillog_str():
    assert str(EmailLog(email="example@example.invalid")) == "example@example.invalid"


def test_generate_token():
    # No really interesting tests we can do here; just make sure it's
    # returning something.
    token = generate_token()
    assert isinstance(token, str)
    assert len(token) == 8

    # ...and that we haven't done something terminally bad.
    assert generate_token() != token
