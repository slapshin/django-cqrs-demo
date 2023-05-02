from decouple import config

ROOT_URLCONF = "src.urls"
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

WSGI_APPLICATION = "src.wsgi.application"
