SECRET_KEY = "test.key"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postrges",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "postgres",
    },
}

CELERY_TASK_ALWAYS_EAGER = True

BASE_URL = "http://localhost:8000"
