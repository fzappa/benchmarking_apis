# ninja_project/settings.py
SECRET_KEY = "test"
DEBUG = True
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "ninja_project.urls"
INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes", "api"]
# MIDDLEWARE = ["django.middleware.common.CommonMiddleware"]
MIDDLEWARE = []
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}