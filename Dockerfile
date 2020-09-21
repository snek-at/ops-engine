FROM python:3.7-slim

LABEL description="This container serves as an entry point for our future Django projects."

# Developed for Werbeagentur Christian Aichner by Florian Kleber
# for terms of use have a look at the LICENSE file.
MAINTAINER Florian Kleber <kleberbaum@erebos.xyz>

# Add custom environment variables needed by Django or your settings file here:
ENV DJANGO_DEBUG=on \
    DJANGO_SETTINGS_MODULE=esite.settings.production

# The uWSGI configuration (customize as needed):
ENV UWSGI_VIRTUALENV=/venv \
	UWSGI_UID=1000 \
	UWSGI_GID=2000 \
	UWSGI_WSGI_FILE=esite/wsgi_production.py \
	UWSGI_HTTP=:8000 \
	UWSGI_MASTER=1 \
	UWSGI_WORKERS=2 \
	UWSGI_THREADS=1

WORKDIR /code/

# Add pre-installation requirements:
ADD requirements/ /requirements/

# Install packages needed to run your application (not build deps):
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN echo "## Installing RUN dependencies ##" && \
    RUN_DEPS=" \
    tini \
    bash \
    libexpat1 \
    libjpeg62-turbo \
    libpcre3 \
    libpq5 \
    mime-support \
    postgresql-client \
    procps \
    zlib1g \
    cron \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

ADD requirements/ /requirements/

RUN echo "## Installing BUILD dependencies ##" && \
    BUILD_DEPS=" \
    build-essential \
    git \
    libexpat1-dev \
    libjpeg62-turbo-dev \
    libpcre3-dev \
    libpq-dev \
    zlib1g-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && python3.7 -m venv /venv \
    && /venv/bin/pip install -U pip \
    && /venv/bin/pip install --no-cache-dir -r /requirements/production.txt \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/* 
EXPOSE 8000

VOLUME /code/media

ADD . /code/


## Place init, make it executable and
# make sure venv files can be used by uWSGI process:
RUN mv /code/docker-entrypoint.sh / ;\
    chmod +x /docker-entrypoint.sh ;\
    find /venv/ -type f -iname "*.py" -exec chmod -v +x {} ;\
    \
    # Call collectstatic with dummy environment variables:
    DATABASE_URL=postgres://none REDIS_URL=none /venv/bin/python manage.py collectstatic --noinput

# I personally like to start my containers with tini
# which start uWSGI, using a wrapper script to allow us to easily add
# more commands to container startup:
ENTRYPOINT ["/usr/bin/tini", "--", "/docker-entrypoint.sh"]

CMD ["/venv/bin/uwsgi", "--http-auto-chunked", \
                        "--http-keepalive", \
                        "--static-map", \
                        "/media/=/code/media/"\
]

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
