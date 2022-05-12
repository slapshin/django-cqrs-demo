#! /bin/bash

set -o errexit

./manage.py migrate

nginx

_UWSGI_OPTS="--ini docker/server/uwsgi.ini"
if [ "${UWSGI_PROCESSES_AUTO:-}" == "1" ]; then
  _UWSGI_OPTS="${_UWSGI_OPTS} --processes $(nproc)"
fi

uwsgi $_UWSGI_OPTS
