# drf_project/urls.py
from django.urls import path, include

urlpatterns = [
    path("", include("api.urls")),
]
