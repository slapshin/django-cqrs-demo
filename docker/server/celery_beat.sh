#! /bin/bash

rm -f /var/run/app/celerybeat.pid

celery -A server.celery_app beat \
        -s /var/run/app/celerybeat.schedule \
        --pidfile /var/run/app/celerybeat.pid
