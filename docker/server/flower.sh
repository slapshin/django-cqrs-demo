#! /bin/bash

set -o errexit

_CELERY_OPTS="-A server.celery_app flower --url_prefix=admin/flower"

celery ${_CELERY_OPTS}

