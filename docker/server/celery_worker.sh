#! /bin/bash

set -o errexit

_CELERY_OPTS="-A server.celery_app worker"
if [ "${CELERY_CONCURRENCY:-}" != "" ]
then
  _CELERY_OPTS="${_CELERY_OPTS} --concurrency ${CELERY_CONCURRENCY}"
fi

if [ "${CELERY_QUEUES:-}" != "" ]
then
  _CELERY_OPTS="${_CELERY_OPTS} -Q ${CELERY_QUEUES}"
fi

celery ${_CELERY_OPTS}
