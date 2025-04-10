# ninja_project/urls.py
from django.urls import path
from ninja import NinjaAPI
from api.views import router

api = NinjaAPI()
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]
