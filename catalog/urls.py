from django.urls import path, include
from catalog.apps import CatalogConfig
from . import views
from .views import products_list, products_detail
app_name = CatalogConfig.name

urlpatterns = [
    path("", products_list, name='products_list'),
    path("products/<int:pk>/", products_detail, name='products_detail'),
    path('contacts/', views.contact_us, name='contacts'),
    path('add_product', views.add_product, name='add_product')
]
