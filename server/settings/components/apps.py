INSTALLED_APPS = (
    # Default django apps:
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # django-admin:
    "django.contrib.admin",
    "django.contrib.admindocs",
    # vendors
    "django_extensions",
    "django_filters",
    "rest_framework",
    "corsheaders",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "crispy_forms",
    "crispy_bootstrap5",
    # apps
    "apps.core",
    "apps.users",
    "apps.blogs",
)
