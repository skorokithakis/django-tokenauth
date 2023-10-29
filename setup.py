#!/usr/bin/env python
import sys

from tokenauth import __version__

assert sys.version_info >= (3, 8), "Requires Python v3.8 or above."
from distutils.core import setup  # noqa
from setuptools import find_namespace_packages  # noqa

setup(
    name="django-tokenauth",
    version=__version__,
    author="Stavros Korokithakis",
    author_email="hi@stavros.io",
    url="https://github.com/skorokithakis/django-tokenauth",
    description="""An authentication backend that uses tokens sent over email to authenticate users.""",
    long_description="A small Django authentication backend that sends users a one-time login link"
    " through email. When the user clicks the link, they are immediately logged in.",
    license="BSD",
    keywords="django",
    zip_safe=False,
    include_package_data=True,
    packages=find_namespace_packages(exclude=("tests",)),
    extras_require={
        "test": [
            "django",
            "black==23.10.1",
            "factory-boy==3.3.0",
            "psycopg2-binary==2.8.6",
            "pytest==7.4.3",
            "pytest-django==4.5.2",
        ],
    },
)
