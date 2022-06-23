#! /bin/bash

set -o errexit

./manage.py migrate

nginx

gunicorn server.asgi:application -k uvicorn.workers.UvicornWorker