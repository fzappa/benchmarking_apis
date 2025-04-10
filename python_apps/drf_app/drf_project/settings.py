# drf_project/settings.py
SECRET_KEY = "test"
DEBUG = True
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "drf_project.urls"
INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes", "rest_framework", "api"]
MIDDLEWARE = []
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}