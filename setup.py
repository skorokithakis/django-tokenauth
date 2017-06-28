#!/usr/bin/env python

import sys
from tokenauth import __version__
assert sys.version >= '2.7', "Requires Python v2.7 or above."
from distutils.core import setup
from setuptools import find_packages

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
    packages=find_packages(),
)
