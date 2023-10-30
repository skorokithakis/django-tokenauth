from io import StringIO

import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_no_migrations_need_creating():
    stdout = StringIO()
    stderr = StringIO()
    call_command("makemigrations", "--check", "--dry-run", stderr=stderr, stdout=stdout)
    assert stderr.getvalue() == ""
    assert "No changes detected" in stdout.getvalue()
