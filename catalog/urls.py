from django.urls import path, include
from catalog.apps import CatalogConfig
from . import views
from .views import ProductListView, ProductDetailView, ContactTemplateView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name='products_list'),
    path("catalog/products/<int:pk>/", ProductDetailView.as_view(), name='products_detail'),
    path('catalog/contacts/', ContactTemplateView.as_view(), name='contacts'),
    path('catalog/create/', ProductCreateView.as_view(), name='product_create'),
    path('catalog/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('catalog/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product')
]
