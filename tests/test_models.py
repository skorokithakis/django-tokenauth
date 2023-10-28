from tokenauth.models import EmailLog, generate_token


def test_emaillog_str():
    assert str(EmailLog(email='example@example.invalid')) == 'example@example.invalid'
