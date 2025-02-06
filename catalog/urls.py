from django.urls import path, include
from catalog.apps import CatalogConfig
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", views.home_view, name="home"),
    path("contacts/", views.contacts_view, name="contacts"),
]
