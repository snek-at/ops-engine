"""
Django production settings for esite project.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/

This development settings are unsuitable for production, see
https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
"""

import random
import string

import dj_database_url

from .base import *


# > Debug Switch
# SECURITY WARNING: don't run with debug turned on in production!
# IMPORTANT: Specified in the environment or set to default (off).
# See https://docs.djangoproject.com/en/stable/ref/settings/#debug
DEBUG = env.get("DJANGO_DEBUG", "off") == "on"

# This is used by Wagtail's email notifications for constructing absolute
# URLs. Please set to the domain that users will access the admin site.
if "PRIMARY_HOST" in env:
    BASE_URL = "https://{}".format(env["PRIMARY_HOST"])

# > Secret Key
# SECURITY WARNING: keep the secret key used in production secret!
# IMPORTANT: Specified in the environment or generate an ephemeral key.
# See https://docs.djangoproject.com/en/stable/ref/settings/#secret-key
if "DJANGO_SECRET_KEY" in env:
    SECRET_KEY = env["DJANGO_SECRET_KEY"]
else:
    # Use if/else rather than a default value to avoid calculating this,
    # if we don't need it.
    print(
        "WARNING: DJANGO_SECRET_KEY not found in os.environ. Generating ephemeral SECRET_KEY."
    )
    SECRET_KEY = "".join(
        [random.SystemRandom().choice(string.printable) for i in range(50)]
    )

# > Allowed Hosts
# Accept all hostnames, since we don't know in advance
# which hostname will be used for any given Docker instance.
# IMPORTANT: Set this to a real hostname when using this in production!
# See https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.get("DJANGO_ALLOWED_HOSTS", "*").split(";")
# > Email Settings
# We use SMTP to send emails. We typically use transactional email services
# that let us use SMTP.
# https://docs.djangoproject.com/en/2.1/topics/email/

# https://docs.djangoproject.com/en/stable/ref/settings/#email-host
if "DJANGO_EMAIL_HOST" in env:
    EMAIL_HOST = env["DJANGO_EMAIL_HOST"]

# https://docs.djangoproject.com/en/stable/ref/settings/#email-port
if "DJANGO_EMAIL_PORT" in env:
    try:
        EMAIL_PORT = int(env["DJANGO_EMAIL_PORT"])
    except ValueError:
        pass

# https://docs.djangoproject.com/en/stable/ref/settings/#email-host-user
if "DJANGO_EMAIL_HOST_USER" in env:
    EMAIL_HOST_USER = env["DJANGO_EMAIL_HOST_USER"]

# https://docs.djangoproject.com/en/stable/ref/settings/#email-host-password
if "DJANGO_EMAIL_HOST_PASSWORD" in env:
    EMAIL_HOST_PASSWORD = env["DJANGO_EMAIL_HOST_PASSWORD"]

# https://docs.djangoproject.com/en/stable/ref/settings/#email-use-tls
if env.get("DJANGO_EMAIL_USE_TLS", "false").lower().strip() == "true":
    EMAIL_USE_TLS = True

# https://docs.djangoproject.com/en/stable/ref/settings/#email-use-ssl
if env.get("DJANGO_EMAIL_USE_SSL", "false").lower().strip() == "true":
    EMAIL_USE_SSL = True

# https://docs.djangoproject.com/en/stable/ref/settings/#email-subject-prefix
if "DJANGO_EMAIL_SUBJECT_PREFIX" in env:
    EMAIL_SUBJECT_PREFIX = env["DJANGO_EMAIL_SUBJECT_PREFIX"]

# SERVER_EMAIL is used to send emails to administrators.
# https://docs.djangoproject.com/en/stable/ref/settings/#server-email
# DEFAULT_FROM_EMAIL is used as a default for any mail send from the website to
# the users.
# https://docs.djangoproject.com/en/stable/ref/settings/#default-from-email
if "DJANGO_SERVER_EMAIL" in env:
    SERVER_EMAIL = DEFAULT_FROM_EMAIL = env["DJANGO_SERVER_EMAIL"]

# > Database Configuration
# See https://pypi.org/project/dj-database-url/
# See https://docs.djangoproject.com/en/stable/ref/settings/#databases
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)


# > Recaptcha
# These settings are required for the captcha challange to work.
# https://github.com/springload/wagtail-django-recaptcha
if "RECAPTCHA_PUBLIC_KEY" in env and "RECAPTCHA_PRIVATE_KEY" in env:
    NOCAPTCHA = True
    RECAPTCHA_PUBLIC_KEY = env["RECAPTCHA_PUBLIC_KEY"]
    RECAPTCHA_PRIVATE_KEY = env["RECAPTCHA_PRIVATE_KEY"]

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
