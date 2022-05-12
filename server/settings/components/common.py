from decouple import config

ROOT_URLCONF = "server.urls"
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

WSGI_APPLICATION = "server.wsgi.application"
