JWT_SECRET_KEY = "test"

INSTALLED_APPS = [
    "django_ninja_jwt_basic",
    "django.contrib.auth",
    "django.contrib.contenttypes",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}
